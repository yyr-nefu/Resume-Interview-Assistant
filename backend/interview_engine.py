import json
import os
import uuid
from typing import List, Dict, Any

class InterviewEngine:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.sessions = {}
        
        self.question_bank = {
            'dev': {
                'basic': [
                    {'question': '请介绍一下你熟悉的编程语言及其应用场景', 'category': 'technical'},
                    {'question': '什么是RESTful API？请举例说明', 'category': 'technical'},
                    {'question': '请解释数据库索引的作用', 'category': 'technical'},
                    {'question': '什么是面向对象编程？有哪些特性？', 'category': 'technical'},
                    {'question': '如何处理并发编程中的线程安全问题？', 'category': 'technical'}
                ],
                'advanced': [
                    {'question': '请设计一个高并发系统的架构方案', 'category': 'technical'},
                    {'question': '微服务架构有哪些优缺点？如何保证服务间通信的可靠性？', 'category': 'technical'},
                    {'question': '分布式系统中如何实现数据一致性？', 'category': 'technical'},
                    {'question': '请分析Redis在缓存中的应用及缓存策略', 'category': 'technical'},
                    {'question': '如何进行系统性能优化？举例说明', 'category': 'technical'}
                ],
                'scenario': [
                    {'question': '如果遇到线上系统突然崩溃，你会如何排查问题？', 'category': 'scenario'},
                    {'question': '如何处理用户反馈的性能问题？', 'category': 'scenario'},
                    {'question': '当需求变更频繁时，如何保证代码质量？', 'category': 'scenario'}
                ]
            },
            'product': {
                'basic': [
                    {'question': '什么是产品经理？主要职责是什么？', 'category': 'technical'},
                    {'question': '如何进行用户需求分析？', 'category': 'technical'},
                    {'question': '产品设计的基本原则有哪些？', 'category': 'technical'},
                    {'question': '如何撰写PRD文档？', 'category': 'technical'},
                    {'question': '什么是MVP？为什么重要？', 'category': 'technical'}
                ],
                'advanced': [
                    {'question': '如何制定产品路线图？', 'category': 'technical'},
                    {'question': '产品数据指标体系如何搭建？', 'category': 'technical'},
                    {'question': '如何平衡用户体验与商业目标？', 'category': 'technical'},
                    {'question': '面对竞品压力，如何制定差异化策略？', 'category': 'technical'},
                    {'question': '如何推动跨团队协作完成产品目标？', 'category': 'technical'}
                ],
                'scenario': [
                    {'question': '如果开发团队认为需求无法实现，你会如何处理？', 'category': 'scenario'},
                    {'question': '用户反馈与数据指标不一致时，你会如何判断？', 'category': 'scenario'},
                    {'question': '如何应对紧急需求与日常迭代的冲突？', 'category': 'scenario'}
                ]
            },
            'data': {
                'basic': [
                    {'question': 'SQL中join有哪些类型？请举例说明', 'category': 'technical'},
                    {'question': '数据仓库和数据库的区别是什么？', 'category': 'technical'},
                    {'question': '什么是ETL？流程是什么？', 'category': 'technical'},
                    {'question': '数据分析的基本流程是什么？', 'category': 'technical'},
                    {'question': '常用的数据可视化工具有哪些？', 'category': 'technical'}
                ],
                'advanced': [
                    {'question': '如何构建数据指标体系？', 'category': 'technical'},
                    {'question': '数据质量如何保证？有哪些监控方法？', 'category': 'technical'},
                    {'question': '机器学习模型在数据分析中的应用场景有哪些？', 'category': 'technical'},
                    {'question': '如何处理大数据量的查询优化？', 'category': 'technical'},
                    {'question': '数据脱敏有哪些方法？', 'category': 'technical'}
                ],
                'scenario': [
                    {'question': '当数据结果与业务直觉不符时，你会如何处理？', 'category': 'scenario'},
                    {'question': '如何向非技术人员解释复杂的数据结论？', 'category': 'scenario'},
                    {'question': '数据需求排期紧张时，如何保证交付质量？', 'category': 'scenario'}
                ]
            },
            'implementation': {
                'basic': [
                    {'question': '项目实施的基本流程是什么？', 'category': 'technical'},
                    {'question': '如何进行项目进度跟踪？', 'category': 'technical'},
                    {'question': '客户沟通的注意事项有哪些？', 'category': 'technical'},
                    {'question': '系统部署的基本步骤是什么？', 'category': 'technical'},
                    {'question': '如何编写技术文档？', 'category': 'technical'}
                ],
                'advanced': [
                    {'question': '如何管理多个并行项目？', 'category': 'technical'},
                    {'question': '如何处理项目风险？举例说明', 'category': 'technical'},
                    {'question': '客户满意度如何提升？', 'category': 'technical'},
                    {'question': '如何进行跨部门协调？', 'category': 'technical'},
                    {'question': '项目验收的标准是什么？', 'category': 'technical'}
                ],
                'scenario': [
                    {'question': '客户现场突发问题如何处理？', 'category': 'scenario'},
                    {'question': '项目延期时如何与客户沟通？', 'category': 'scenario'},
                    {'question': '如何应对客户不合理的需求变更？', 'category': 'scenario'}
                ]
            }
        }
        
    def start_interview(self, jd_id: str, question_count: int, difficulty_ratio: str) -> Dict[str, Any]:
        jd_path = os.path.join(self.data_dir, f"{jd_id}.json")
        if not os.path.exists(jd_path):
            raise ValueError("JD不存在")
        
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_data = json.load(f)
        
        position_type = jd_data['position_type']
        bank = self.question_bank.get(position_type, self.question_bank['dev'])
        
        basic_count = question_count // 2
        advanced_count = question_count // 2
        scenario_count = question_count - basic_count - advanced_count
        
        if difficulty_ratio == 'basic':
            basic_count = question_count - 1
            advanced_count = 1
            scenario_count = 0
        elif difficulty_ratio == 'advanced':
            basic_count = 1
            advanced_count = question_count - 2
            scenario_count = 1
        
        questions = []
        question_id = 1
        
        for q in bank['basic'][:basic_count]:
            questions.append({
                'id': f"q{question_id}",
                'question': q['question'],
                'type': 'basic',
                'category': q['category']
            })
            question_id += 1
        
        for q in bank['advanced'][:advanced_count]:
            questions.append({
                'id': f"q{question_id}",
                'question': q['question'],
                'type': 'advanced',
                'category': q['category']
            })
            question_id += 1
        
        for q in bank['scenario'][:scenario_count]:
            questions.append({
                'id': f"q{question_id}",
                'question': q['question'],
                'type': 'advanced',
                'category': q['category']
            })
            question_id += 1
        
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'jd_id': jd_id,
            'position_type': position_type,
            'questions': questions,
            'answers': {},
            'started_at': str(pd.Timestamp.now())
        }
        
        return {
            'session_id': session_id,
            'questions': questions
        }
        
    def submit_answer(self, session_id: str, question_id: str, answer: str) -> Dict[str, Any]:
        if session_id not in self.sessions:
            raise ValueError("会话不存在")
        
        self.sessions[session_id]['answers'][question_id] = answer
        
        with open(os.path.join(self.data_dir, f"interview_{session_id}.json"), 'w', encoding='utf-8') as f:
            json.dump(self.sessions[session_id], f, ensure_ascii=False)
        
        return {'status': 'success'}