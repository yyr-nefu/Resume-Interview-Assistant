from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
from datetime import datetime
from jd_parser import JDParser
from resume_analyzer import ResumeAnalyzer
from resume_optimizer import ResumeOptimizer
from interview_engine import InterviewEngine
from interview_reviewer import InterviewReviewer
from note_generator import NoteGenerator
from archive_manager import ArchiveManager

app = FastAPI(title="AI求职赋能助手", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jd_parser = JDParser()
resume_analyzer = ResumeAnalyzer()
resume_optimizer = ResumeOptimizer()
interview_engine = InterviewEngine()
interview_reviewer = InterviewReviewer()
note_generator = NoteGenerator()
archive_manager = ArchiveManager()

class JDParseRequest(BaseModel):
    jd_content: str
    position_type: str  # dev, product, data, implementation

class JDParseResponse(BaseModel):
    technical_skills: List[str]
    soft_skills: List[str]
    position_knowledge: List[str]
    basic_requirements: List[str]
    bonus_points: List[str]

class ResumeAnalysisRequest(BaseModel):
    resume_content: str
    jd_id: Optional[str] = None
    jd_content: Optional[str] = None

class ResumeAnalysisResponse(BaseModel):
    matched_skills: List[str]
    gap_skills: List[str]
    bonus_opportunities: List[str]
    score: int

class ResumeOptimizeRequest(BaseModel):
    resume_content: str
    jd_id: str
    position_type: str

class ResumeOptimizeResponse(BaseModel):
    optimized_resume: str
    word_count: int
    suggestions: List[str]

class InterviewQuestion(BaseModel):
    id: str
    question: str
    type: str  # basic, advanced
    category: str  # technical, scenario

class InterviewRequest(BaseModel):
    jd_id: str
    question_count: int = 5
    difficulty_ratio: str = "balanced"  # basic, balanced, advanced

class InterviewStartResponse(BaseModel):
    session_id: str
    questions: List[InterviewQuestion]

class InterviewAnswerRequest(BaseModel):
    session_id: str
    question_id: str
    answer: str

class InterviewCompleteRequest(BaseModel):
    session_id: str

class InterviewReviewResponse(BaseModel):
    session_id: str
    professional_score: int
    comprehensive_score: int
    reviews: List[Dict[str, Any]]
    templates: List[str]
    examples: List[str]

class NoteGenerateRequest(BaseModel):
    jd_id: str
    session_id: Optional[str] = None
    gaps: Optional[List[str]] = None

class NoteResponse(BaseModel):
    note_id: str
    content: str
    questions: List[Dict[str, Any]]

class ArchiveItem(BaseModel):
    id: str
    type: str  # resume, interview, note
    name: str
    created_at: str
    jd_id: str

class ArchiveResponse(BaseModel):
    items: List[ArchiveItem]

@app.post("/api/jd/parse", response_model=JDParseResponse)
async def parse_jd(request: JDParseRequest):
    result = jd_parser.parse(request.jd_content, request.position_type)
    return result

@app.post("/api/resume/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(request: ResumeAnalysisRequest):
    result = resume_analyzer.analyze(request.resume_content, request.jd_id, request.jd_content)
    return result

@app.post("/api/resume/optimize", response_model=ResumeOptimizeResponse)
async def optimize_resume(request: ResumeOptimizeRequest):
    result = resume_optimizer.optimize(request.resume_content, request.jd_id, request.position_type)
    return result

@app.post("/api/interview/start", response_model=InterviewStartResponse)
async def start_interview(request: InterviewRequest):
    result = interview_engine.start_interview(request.jd_id, request.question_count, request.difficulty_ratio)
    return result

@app.post("/api/interview/answer")
async def submit_answer(request: InterviewAnswerRequest):
    result = interview_engine.submit_answer(request.session_id, request.question_id, request.answer)
    return result

@app.post("/api/interview/complete", response_model=InterviewReviewResponse)
async def complete_interview(request: InterviewCompleteRequest):
    result = interview_reviewer.review(request.session_id)
    return result

@app.post("/api/note/generate", response_model=NoteResponse)
async def generate_note(request: NoteGenerateRequest):
    result = note_generator.generate(request.jd_id, request.session_id, request.gaps)
    return result

@app.get("/api/archive/list", response_model=ArchiveResponse)
async def list_archive(jd_id: Optional[str] = None):
    result = archive_manager.list_items(jd_id)
    return result

@app.get("/api/archive/get/{item_id}")
async def get_archive_item(item_id: str):
    result = archive_manager.get_item(item_id)
    return result

@app.delete("/api/archive/delete/{item_id}")
async def delete_archive_item(item_id: str):
    result = archive_manager.delete_item(item_id)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)