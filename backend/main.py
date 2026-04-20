from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.research_agent import research_company
from agents.planner_agent import plan_research

app = FastAPI()

# CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Intellex backend running"}

@app.post("/research")
def research(data: dict):
    return {"result": research_company(data["company"], data["persona"])}

@app.post("/planner")
def planner(data: dict):
    return {"result": plan_research(data["question"])}