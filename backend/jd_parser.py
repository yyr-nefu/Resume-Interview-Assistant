import json
import os
from typing import List, Dict, Any

class JDParser:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.jd_store = {}
        
    def parse(self, jd_content: str, position_type: str) -> Dict[str, Any]:
        technical_keywords = {
            'dev': ['Python', 'Java', 'JavaScript', 'React', 'Vue', 'Spring', 'MySQL', 'Redis', 'Docker', 'Git', '算法', '数据结构', '后端', '前端', '全栈', '微服务', 'RESTful'],
            'product': ['需求分析', '产品设计', '原型设计', '用户研究', '数据分析', 'PRD', '产品文档', '敏捷开发', '竞品分析', '用户体验', 'MVP', '迭代'],
            'data': ['SQL', 'Python', '数据分析', '数据挖掘', '机器学习', 'Excel', 'Tableau', '数据仓库', 'ETL', '统计学', 'BI', '数据可视化'],
            'implementation': ['项目管理', '需求沟通', '进度跟踪', '问题排查', '客户支持', '文档编写', '系统部署', '运维', '测试', '培训']
        }
        
        soft_keywords = ['沟通能力', '团队协作', '学习能力', '抗压能力', '责任心', '执行力', '逻辑思维', '创新能力', '英语能力']
        
        position_keywords = {
            'dev': ['计算机', '软件工程', '编程', '开发', '技术', '代码', '系统', '架构'],
            'product': ['产品', '互联网', '用户', '市场', '需求', '设计', '体验'],
            'data': ['数据', '分析', '统计', '挖掘', '报表', 'BI', '可视化'],
            'implementation': ['项目', '实施', '交付', '运维', '客户', '部署']
        }
        
        jd_lower = jd_content.lower()
        tech_skills = [k for k in technical_keywords.get(position_type, []) if k.lower() in jd_lower or k in jd_content]
        soft_skills = [k for k in soft_keywords if k in jd_content]
        position_knowledge = [k for k in position_keywords.get(position_type, []) if k.lower() in jd_lower or k in jd_content]
        
        basic_requirements = []
        bonus_points = []
        
        if '本科' in jd_content:
            basic_requirements.append('本科学历')
        if '硕士' in jd_content:
            basic_requirements.append('硕士学历')
        if '应届生' in jd_content:
            basic_requirements.append('应届生身份')
        if '英语' in jd_content:
            basic_requirements.append('英语能力')
        
        if '实习' in jd_content:
            bonus_points.append('相关实习经历')
        if '项目' in jd_content:
            bonus_points.append('项目经验')
        if '竞赛' in jd_content:
            bonus_points.append('竞赛获奖')
        if '开源' in jd_content:
            bonus_points.append('开源项目贡献')
        
        basic_requirements.extend(tech_skills[:3])
        bonus_points.extend(tech_skills[3:])
        
        result = {
            'technical_skills': tech_skills,
            'soft_skills': soft_skills,
            'position_knowledge': position_knowledge,
            'basic_requirements': basic_requirements[:5],
            'bonus_points': bonus_points[:5]
        }
        
        jd_id = f"jd_{len(self.jd_store) + 1}"
        self.jd_store[jd_id] = {
            'content': jd_content,
            'position_type': position_type,
            'parsed': result,
            'created_at': str(pd.Timestamp.now())
        }
        
        with open(os.path.join(self.data_dir, f"{jd_id}.json"), 'w', encoding='utf-8') as f:
            json.dump(self.jd_store[jd_id], f, ensure_ascii=False)
        
        return result