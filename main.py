from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
import time
from datetime import datetime

from crewai import Crew, Process

from database import users_collection, analysis_collection
from agents import (
    financial_analyst,
    verifier,
    investment_advisor,
    risk_assessor
)
from task import (
    verification,
    analyze_financial_document as financial_analysis_task,
    investment_analysis,
    risk_assessment
)

from tools import read_pdf


app = FastAPI(title="Financial Document Analyzer (Optimized)")

def summarize_document(text: str) -> str:
    """
    Compress financial document to reduce token usage.
    """

    prompt = f"""
    Summarize the following financial document into a structured financial brief.

    Extract only:
    - Revenue
    - Net income
    - Operating margin
    - Cash flow
    - Growth trends
    - Major financial risks

    Limit response to 700 words.
    
    Document:
    {text}
    """

    # Direct LLM call (single summarization step)
    return financial_analyst.llm.call(prompt)


def run_crew(query: str, path: str):

 
    full_text = read_pdf(path)

    
    financial_summary = summarize_document(full_text)

    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[
            verification,
            financial_analysis_task,
            investment_analysis,
            risk_assessment
        ],
        process=Process.sequential,
    )

 
    for attempt in range(3):
        try:
            result = financial_crew.kickoff({
                "query": query,
                "financial_summary": financial_summary
            })

            if result is None:
                raise Exception("Crew returned empty result")

            return result

        except Exception as e:
            if "rate_limit" in str(e).lower():
                time.sleep(2)
            else:
                raise e

    raise Exception("Rate limit exceeded after retries")



@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}



@app.post("/create-user")
def create_user(name: str = Form(...), email: str = Form(...)):
    user_id = str(uuid.uuid4())

    users_collection.insert_one({
        "user_id": user_id,
        "name": name,
        "email": email,
        "created_at": datetime.utcnow()
    })

    return {
        "message": "User created successfully",
        "user_id": user_id
    }



@app.post("/analyze")
async def analyze_document(
    user_id: str = Form(...),
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    job_id = str(uuid.uuid4())
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)

        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        if not query:
            query = "Analyze this financial document for investment insights"

        # Insert job (processing state)
        analysis_collection.insert_one({
            "job_id": job_id,
            "user_id": user_id,
            "file_name": file.filename,
            "query": query,
            "status": "processing",
            "created_at": datetime.utcnow()
        })

        # Run Crew in background thread
        response = await asyncio.to_thread(
            run_crew,
            query=query.strip(),
            path=file_path
        )

        # Update DB with result
        analysis_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "completed",
                    "analysis": str(response),
                    "completed_at": datetime.utcnow()
                }
            }
        )

        return {
            "message": "Analysis completed",
            "job_id": job_id
        }

    except Exception as e:

        analysis_collection.update_one(
            {"job_id": job_id},
            {
                "$set": {
                    "status": "failed",
                    "error": str(e),
                    "completed_at": datetime.utcnow()
                }
            }
        )

        raise HTTPException(
            status_code=500,
            detail=f"Error processing financial document: {str(e)}"
        )

    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

@app.get("/result/{job_id}")
def get_result(job_id: str):

    result = analysis_collection.find_one(
        {"job_id": job_id},
        {"_id": 0}
    )

    if not result:
        raise HTTPException(status_code=404, detail="Job not found")

    return result



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)