import json
import os
import uuid
from typing import List, Dict, Any, Optional

class NoteGenerator:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.knowledge_base = {
            'dev': {
                'core_topics': ['数据结构与算法', '数据库原理', '操作系统', '计算机网络', '设计模式'],
                'practice_questions': [
                    {'question': '实现快速排序算法', 'difficulty': 'medium'},
                    {'question': '设计一个线程安全的缓存系统', 'difficulty': 'hard'},
                    {'question': '解释TCP三次握手过程', 'difficulty': 'easy'}
                ]
            },
            'product': {
                'core_topics': ['用户研究方法', '产品设计流程', '数据分析方法', '项目管理', '竞品分析'],
                'practice_questions': [
                    {'question': '如何设计一个电商APP的首页', 'difficulty': 'medium'},
                    {'question': '制定一款社交产品的增长策略', 'difficulty': 'hard'},
                    {'question': '用户调研有哪些方法？', 'difficulty': 'easy'}
                ]
            },
            'data': {
                'core_topics': ['SQL进阶', '统计学基础', '数据仓库设计', '数据可视化', '机器学习入门'],
                'practice_questions': [
                    {'question': '编写SQL查询找出每月销售额Top10的商品', 'difficulty': 'medium'},
                    {'question': '设计一个用户行为分析的数据模型', 'difficulty': 'hard'},
                    {'question': '解释什么是A/B测试', 'difficulty': 'easy'}
                ]
            },
            'implementation': {
                'core_topics': ['项目管理方法论', '客户沟通技巧', '系统部署流程', '问题排查方法', '文档编写规范'],
                'practice_questions': [
                    {'question': '制定一个项目实施计划', 'difficulty': 'medium'},
                    {'question': '如何处理客户的紧急问题', 'difficulty': 'hard'},
                    {'question': '技术文档包含哪些部分？', 'difficulty': 'easy'}
                ]
            }
        }
        
    def generate(self, jd_id: str, session_id: Optional[str] = None, gaps: Optional[List[str]] = None) -> Dict[str, Any]:
        jd_path = os.path.join(self.data_dir, f"{jd_id}.json")
        if not os.path.exists(jd_path):
            raise ValueError("JD不存在")
        
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_data = json.load(f)
        
        position_type = jd_data['position_type']
        parsed_jd = jd_data['parsed']
        knowledge = self.knowledge_base.get(position_type, self.knowledge_base['dev'])
        
        wrong_answers = []
        if session_id:
            session_path = os.path.join(self.data_dir, f"interview_{session_id}.json")
            if os.path.exists(session_path):
                with open(session_path, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                for q in session_data['questions']:
                    answer = session_data['answers'].get(q['id'], '')
                    if len(answer) < 50:
                        wrong_answers.append(q['question'])
        
        note_content = f"# {position_type}岗位学习笔记\n\n"
        note_content += "## 一、JD能力缺口分析\n"
        if gaps:
            note_content += "\n".join([f"- {gap}" for gap in gaps])
        else:
            note_content += "暂无明确缺口，建议根据JD要求补充相关技能\n"
        
        note_content += "\n## 二、错题汇总\n"
        if wrong_answers:
            note_content += "\n".join([f"- {q}" for q in wrong_answers])
        else:
            note_content += "暂无错题记录\n"
        
        note_content += "\n## 三、核心知识点\n"
        note_content += "\n".join([f"- {topic}" for topic in knowledge['core_topics']])
        
        note_content += "\n## 四、答题模板\n"
        note_content += "1. 技术类问题：问题分析 → 核心思路 → 具体实现 → 总结反思\n"
        note_content += "2. 情景类问题：理解问题 → 分析原因 → 解决方案 → 预期效果\n"
        
        note_content += "\n## 五、配套练习题\n"
        for idx, q in enumerate(knowledge['practice_questions'], 1):
            note_content += f"{idx}. {q['question']}（难度：{q['difficulty']}）\n"
        
        note_id = str(uuid.uuid4())
        note_data = {
            'note_id': note_id,
            'jd_id': jd_id,
            'position_type': position_type,
            'content': note_content,
            'created_at': str(pd.Timestamp.now()),
            'questions': knowledge['practice_questions']
        }
        
        with open(os.path.join(self.data_dir, f"note_{note_id}.json"), 'w', encoding='utf-8') as f:
            json.dump(note_data, f, ensure_ascii=False)
        
        return {
            'note_id': note_id,
            'content': note_content,
            'questions': knowledge['practice_questions']
        }