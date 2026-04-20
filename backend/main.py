from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

from agents.research_agent import research_company
from agents.planner_agent import plan_research
from agents.document_agent import ask_document
from core.llm import ask_llm
from core.prompts import comparison_prompt


app = FastAPI()

# -------- CORS (REACT) --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- REQUEST MODELS --------

class ResearchReq(BaseModel):
    company: str
    persona: str
    query: str | None = None   

class PlannerReq(BaseModel):
    problem: str

class DocsReq(BaseModel):
    question: str
    content: str

class CompareReq(BaseModel):
    company1: str
    company2: str


# -------- ROUTES --------

@app.post("/research")

def research(req: ResearchReq):
    try:
        result = research_company(
            req.company,
            req.persona,
            req.query
        )
        return {"result": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/planner")
def planner(req: PlannerReq):
    try:
        result = plan_research(req.problem)
        return {"result": result}
    except Exception as e:
        return {"result": f"Error: {str(e)}"}



@app.post("/docs")
def docs(req: DocsReq):
    try:
        result = ask_document(req.question, req.content)
        return {"result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare")
def compare(req: CompareReq):
    try:
        r1 = research_company(req.company1)
        r2 = research_company(req.company2)

        res = ask_llm(
            comparison_prompt(req.company1, req.company2, r1, r2)
        )

        return {"result": res}
    except Exception as e:
        return {"result": f"Error: {str(e)}"}