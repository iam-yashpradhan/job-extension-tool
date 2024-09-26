from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime, timezone
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

port = os.environ.get('PORT', 4000)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
DB_ID = os.environ.get("DB_ID")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

class JobApplication(BaseModel):
    company: str
    position: str

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DB_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    return res.json()

@app.post("/add_job_application")
async def add_job_application(job: JobApplication):
    current_date = datetime.now(timezone.utc).isoformat()
    
    data = {
        "Company": {"title": [{"text": {"content": job.company}}]},
        "Date Applied": {"date": {"start": current_date, "end": None}},
        "Position": {
            "multi_select": [
                {"name": job.position},
            ]
        }
    }
    
    response = create_page(data)
    
    if 'id' in response:
        return {"message": "Job application added successfully", "notion_page_id": response['id']}
    else:
        raise HTTPException(status_code=500, detail="Failed to add job application to Notion")
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 4000))
    uvicorn.run(app, host="0.0.0.0", port=port)