import json
import os
from typing import List, Dict, Any

class ResumeAnalyzer:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(self.data_dir, exist_ok=True)
        from jd_parser import JDParser
        self.jd_parser = JDParser()
        
    def analyze(self, resume_content: str, jd_id: str = None, jd_content: str = None) -> Dict[str, Any]:
        if jd_content:
            parsed_jd = self.jd_parser.parse(jd_content, "dev")
        elif jd_id:
            jd_path = os.path.join(self.data_dir, f"{jd_id}.json")
            if not os.path.exists(jd_path):
                raise ValueError("JD不存在")
            
            with open(jd_path, 'r', encoding='utf-8') as f:
                jd_data = json.load(f)
            
            parsed_jd = jd_data['parsed']
        else:
            raise ValueError("必须提供JD内容或JD ID")
        
        all_jd_skills = parsed_jd['technical_skills'] + parsed_jd['soft_skills']
        
        resume_lower = resume_content.lower()
        matched_skills = []
        gap_skills = []
        
        for skill in all_jd_skills:
            if skill.lower() in resume_lower or skill in resume_content:
                matched_skills.append(skill)
            else:
                gap_skills.append(skill)
        
        bonus_opportunities = [b for b in parsed_jd['bonus_points'] if b.lower() not in resume_lower and b not in resume_content]
        
        score = int((len(matched_skills) / len(all_jd_skills)) * 100) if all_jd_skills else 0
        
        return {
            'matched_skills': matched_skills,
            'gap_skills': gap_skills,
            'bonus_opportunities': bonus_opportunities,
            'score': score
        }