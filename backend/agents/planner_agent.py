from core.llm import ask_llm


# -------- CONFIG --------
PLANNER_SYSTEM = """
You are a senior research strategist.

Your job is to break complex problems into clear, actionable research plans.

Always structure your response properly.
Be concise but structured.
"""


# -------- MAIN FUNCTION --------
def plan_research(question):

    if not question:
        return "❌ Please provide a research question."

    prompt = f"""
    {PLANNER_SYSTEM}

    Create a structured research plan for the following problem.

    Include:

    ## 1. Objectives
    - What needs to be solved

    ## 2. Data Collection
    - What data is required
    - Possible sources

    ## 3. Tools & Methods
    - Techniques / tools to use

    ## 4. Analysis Steps
    - Step-by-step execution plan

    ## 5. Risks & Challenges
    - Potential issues

    ## 6. Expected Outcome
    - What the result should look like

    Question:
    {question}

    IMPORTANT:
    - Use clear headings
    - Use bullet points
    - Keep it structured and readable
    """

    return ask_llm(prompt)