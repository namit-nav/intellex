from core.llm import ask_llm


# -------- CONFIG --------
PLANNER_SYSTEM = """
You are a senior research strategist.

Break complex problems into structured, actionable research plans.

Rules:
- Be concise but insightful
- Avoid vague statements
- Do NOT add unnecessary explanations
- Focus on clarity and execution
"""


# -------- MAIN FUNCTION --------
def plan_research(question):

    if not question:
        return "Please provide a research question."

    prompt = f"""
{PLANNER_SYSTEM}

Create a structured research plan for the following problem.

Formatting Rules (IMPORTANT):
- Use "## " for headings
- Use "- " for bullet points
- Keep sections clean and readable

Output Structure:

## Objectives
- What needs to be solved

## Data Collection
- Required data
- Possible sources

## Tools & Methods
- Techniques and tools

## Analysis Steps
- Step-by-step execution

## Risks & Challenges
- Potential issues

## Expected Outcome
- Final deliverables

Problem:
{question}
"""

    return ask_llm(prompt)