import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.dependencies import get_current_user
from app.db.models.user import User
from app.db.models.job import Job
from app.db.session import get_db
from app.schemas.research import ResearchRequest, JobCreateResponse, JobStatusResponse
from app.tasks.research_tasks import run_research_job

router = APIRouter(
    prefix="/research",
    tags=["Research"],
)


@router.post(
    "",
    response_model=JobCreateResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Enqueue an AI-powered research workflow",
)
async def create_research_job(
    request: ResearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobCreateResponse:
    """
    Creates a job record, enqueues the research task to Celery, and returns immediately.
    """
    job_id = str(uuid.uuid4())
    
    # Create the job record in the database
    job = Job(
        job_id=job_id,
        user_id=current_user.id,
        query=request.query,
        status="queued"
    )
    db.add(job)
    await db.commit()

    # Trigger the Celery task
    run_research_job.delay(job_id, request.query)

    return JobCreateResponse(job_id=job_id, status="queued")


@router.get(
    "/{job_id}/status",
    response_model=JobStatusResponse,
    summary="Get status of an enqueued research job",
)
async def get_job_status(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> JobStatusResponse:
    """
    Returns the live status of the research job, read directly from the database status table.
    """
    result = await db.execute(select(Job).where(Job.job_id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found."
        )

    # Security check: Ensure the user owns this job
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden."
        )

    return JobStatusResponse(
        job_id=job.job_id,
        status=job.status,
        current_node=job.current_node,
        iteration_count=job.iteration_count,
        sufficiency_score=job.sufficiency_score,
        coverage_metrics=job.coverage_metrics,
        updated_at=job.updated_at
    )


@router.get(
    "/{job_id}/result",
    summary="Get final report of a completed research job",
)
async def get_job_result(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the final markdown report for a completed job.
    Returns 409 Conflict if the job is still queued or running.
    """
    result = await db.execute(select(Job).where(Job.job_id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found."
        )

    # Security check
    if job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden."
        )

    if job.status in ("queued", "running"):
        # 409 Conflict (or 425 Too Early) is raised if the resource is not ready yet.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Job is still running."
        )

    if job.status == "failed":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Job failed: {job.error_message}"
        )

    if not job.result_path or not os.path.exists(job.result_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report result file not found."
        )

    return FileResponse(
        path=job.result_path,
        media_type="text/markdown",
        filename=f"research_report_{job_id}.md"
    )