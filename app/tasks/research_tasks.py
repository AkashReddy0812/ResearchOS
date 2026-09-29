import asyncio
import os
from sqlalchemy import select

from app.tasks.celery_app import celery_app
from app.db.session import AsyncSessionLocal
from app.db.models.job import Job
from app.ai.workflows.graph import research_graph


async def run_research_workflow(job_id: str, query: str):
    """
    Executes the LangGraph research workflow asynchronously,
    streaming node updates to the database.
    """
    state = {
        "query": query,
        "papers": [],
        "pdf_paths": [],
        "documents": [],
        "chunks": [],
        "embeddings": [],
        "retrieved_chunks": [],
        "reranked_chunks": [],
        "context": "",
        "answer": "",
        "citations": [],
        "report": "",
        "errors": [],
    }

    # Set status to running
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Job).where(Job.job_id == job_id))
        job = result.scalar_one_or_none()
        if job:
            job.status = "running"
            job.current_node = "planner"
            await session.commit()

    try:
        # Stream events from LangGraph
        async for event in research_graph.astream(state, stream_mode="updates"):
            # Update database with current node
            for node_name, values in event.items():
                # Accumulate state updates
                if isinstance(values, dict):
                    for k, v in values.items():
                        state[k] = v

                async with AsyncSessionLocal() as session:
                    result = await session.execute(select(Job).where(Job.job_id == job_id))
                    job = result.scalar_one_or_none()
                    if job:
                        job.current_node = node_name
                        # Update iteration counts and coverage metrics if they exist in state
                        if "iteration_count" in state:
                            job.iteration_count = state["iteration_count"]
                        if "sufficiency_score" in state:
                            job.sufficiency_score = state["sufficiency_score"]
                        if "coverage_metrics" in state:
                            job.coverage_metrics = state["coverage_metrics"]
                        await session.commit()

        # Save the final report and complete the job
        report_dir = "storage/reports"
        os.makedirs(report_dir, exist_ok=True)
        report_path = os.path.join(report_dir, f"{job_id}.md")
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(state.get("report", ""))

        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Job).where(Job.job_id == job_id))
            job = result.scalar_one_or_none()
            if job:
                job.status = "completed"
                job.result_path = report_path
                job.current_node = "END"
                # Update any final metrics
                if "iteration_count" in state:
                    job.iteration_count = state["iteration_count"]
                if "sufficiency_score" in state:
                    job.sufficiency_score = state["sufficiency_score"]
                if "coverage_metrics" in state:
                    job.coverage_metrics = state["coverage_metrics"]
                await session.commit()

    except Exception as e:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Job).where(Job.job_id == job_id))
            job = result.scalar_one_or_none()
            if job:
                job.status = "failed"
                job.error_message = str(e)
                await session.commit()
        raise e


@celery_app.task(name="app.tasks.research_tasks.run_research_job", acks_late=True)
def run_research_job(job_id: str, query: str):
    """
    Celery task wrapper to execute research asynchronously.
    """
    asyncio.run(run_research_workflow(job_id, query))
