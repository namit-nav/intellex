from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from routes.export import router as export_router
from fastapi import UploadFile, File

app = FastAPI()

@app.get("/")

def root():
    return {"message": "Intellex backend is live"}

app.include_router(export_router)

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

class CompareReq(BaseModel):
    company1: str
    company2: str


# -------- ROUTES --------

@app.post("/research")

def research(req: ResearchReq):
    try:
        from agents.research_agent import research_company
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
        from agents.planner_agent import plan_research
        result = plan_research(req.problem)
        return {"result": result}
    except Exception as e:
        return {"result": f"Error: {str(e)}"}



@app.post("/docs")
def docs(req: DocsReq):
    try:
        from agents.document_agent import ask_document
        result = ask_document(req.question)
        return {"result": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/docs-upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    from agents.document_agent import load_document_pdf

    result = load_document_pdf(file.file)

    return {"message": result}


@app.post("/compare")
def compare(req: CompareReq):
    try:
        from agents.research_agent import research_company
        from core.llm import ask_llm
        from core.prompts import comparison_prompt
        r1 = research_company(req.company1)
        r2 = research_company(req.company2)

        res = ask_llm(
            comparison_prompt(req.company1, req.company2, r1, r2)
        )

        return {"result": res}
    except Exception as e:
        return {"result": f"Error: {str(e)}"}