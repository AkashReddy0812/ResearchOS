from app.ai.llm.generator import Generator

from app.ai.workflows.state import ResearchState



generator = Generator()



def answer_generation_node(
    state: ResearchState
) -> ResearchState:
    """
    Generate grounded research answer.
    """


    answer = generator.generate(

        query=state["query"],

        context=state["context"]

    )


    state["answer"] = answer


    return state