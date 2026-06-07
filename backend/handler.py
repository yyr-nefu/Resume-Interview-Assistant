# 阿里云函数计算入口文件
import logging
import os
import sys

# 添加backend目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from jd_parser import JDParser
from resume_analyzer import ResumeAnalyzer
from resume_optimizer import ResumeOptimizer
from interview_engine import InterviewEngine
from interview_reviewer import InterviewReviewer
from note_generator import NoteGenerator
from archive_manager import ArchiveManager

# 禁用Mangum的日志以减少日志量
logging.getLogger("mangum").setLevel(logging.WARNING)

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

# ==================== API路由 ====================

@app.get("/")
async def root():
    return {"message": "AI求职赋能助手 API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/jd/parse")
async def parse_jd(jd_content: str, position_type: str = "dev"):
    try:
        result = jd_parser.parse(jd_content, position_type)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/resume/analyze")
async def analyze_resume(resume_content: str, jd_content: str = None):
    try:
        result = resume_analyzer.analyze(resume_content, jd_content)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/resume/optimize")
async def optimize_resume(resume_content: str, jd_content: str = None):
    try:
        result = resume_optimizer.optimize(resume_content, jd_content)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/interview/start")
async def start_interview(jd: str = ""):
    try:
        session_id, first_question = interview_engine.start_interview(jd)
        return {"success": True, "sessionId": session_id, "question": first_question}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/interview/chat")
async def chat_interview(sessionId: str, message: str):
    try:
        response = interview_engine.chat(sessionId, message)
        return {"success": True, "data": response}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/interview/report/{session_id}")
async def get_report(session_id: str):
    try:
        report = interview_engine.get_report(session_id)
        return {"success": True, "data": report}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/interview/review")
async def review_interview(session_id: str, user_answer: str, question: str):
    try:
        result = interview_reviewer.review(user_answer, question)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/notes/generate")
async def generate_notes(resume_content: str, jd_content: str = None):
    try:
        result = note_generator.generate(resume_content, jd_content)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": str(e)}

# AWS Lambda / 阿里云函数计算入口
handler = Mangum(app, enable_lifespan=False)
