import json
import os
from typing import List, Dict, Any

class ResumeOptimizer:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.position_templates = {
            'dev': {
                'prefix': '负责',
                'verbs': ['设计', '开发', '实现', '优化', '重构', '调试', '部署'],
                'keywords': ['系统', '模块', '功能', '接口', '服务', '算法']
            },
            'product': {
                'prefix': '负责',
                'verbs': ['设计', '规划', '分析', '优化', '迭代', '调研', '推动'],
                'keywords': ['需求', '产品', '功能', '用户', '体验', '数据']
            },
            'data': {
                'prefix': '负责',
                'verbs': ['分析', '挖掘', '建模', '清洗', '可视化', '报告'],
                'keywords': ['数据', '报表', '指标', '分析', '模型', '趋势']
            },
            'implementation': {
                'prefix': '负责',
                'verbs': ['实施', '部署', '培训', '调试', '维护', '协调'],
                'keywords': ['项目', '系统', '客户', '部署', '交付', '运维']
            }
        }
        
    def optimize(self, resume_content: str, jd_id: str, position_type: str) -> Dict[str, Any]:
        jd_path = os.path.join(self.data_dir, f"{jd_id}.json")
        if not os.path.exists(jd_path):
            raise ValueError("JD不存在")
        
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_data = json.load(f)
        
        parsed_jd = jd_data['parsed']
        template = self.position_templates.get(position_type, self.position_templates['dev'])
        
        optimized_sections = []
        suggestions = []
        
        lines = resume_content.split('\n')
        for line in lines:
            if line.strip():
                optimized_line = line
                
                for verb in template['verbs']:
                    if verb in line:
                        optimized_line = f"{template['prefix']}{line}"
                        break
                
                for keyword in parsed_jd['technical_skills'][:3]:
                    if keyword.lower() in line.lower() and keyword not in optimized_line:
                        optimized_line = f"{optimized_line}（涉及{keyword}）"
                
                optimized_sections.append(optimized_line)
        
        optimized_resume = '\n'.join(optimized_sections)
        
        word_count = len(optimized_resume)
        
        if word_count > 2000:
            suggestions.append("简历内容较长，建议精简至2页内")
        if len(parsed_jd['technical_skills']) > 0:
            suggestions.append(f"建议突出以下核心技能：{', '.join(parsed_jd['technical_skills'][:3])}")
        suggestions.append("建议量化项目成果，如'提升效率30%'")
        
        return {
            'optimized_resume': optimized_resume,
            'word_count': word_count,
            'suggestions': suggestions
        }