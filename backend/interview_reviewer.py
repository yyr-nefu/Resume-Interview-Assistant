import json
import os
from typing import List, Dict, Any

class InterviewReviewer:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(self.data_dir, exist_ok=True)
        
        self.evaluation_criteria = {
            'dev': {
                'keywords': ['算法', '数据结构', '复杂度', '优化', '设计模式', '架构', '性能', '安全'],
                'templates': [
                    '回答结构：问题分析 → 核心思路 → 具体实现 → 复杂度分析',
                    '技术方案：需求分析 → 架构设计 → 详细设计 → 测试验证',
                    '问题排查：现象描述 → 假设验证 → 定位根因 → 解决方案'
                ],
                'examples': [
                    '关于并发问题：采用线程池控制并发数，使用锁机制保证数据一致性，通过原子操作减少锁竞争',
                    '关于系统设计：采用微服务架构，使用Redis做缓存，MQ解耦服务，数据库读写分离'
                ]
            },
            'product': {
                'keywords': ['用户', '需求', '数据', '体验', '迭代', '优先级', '竞品'],
                'templates': [
                    '需求分析：用户调研 → 需求梳理 → 优先级排序 → 方案设计',
                    '产品设计：目标用户 → 使用场景 → 功能设计 → 交互设计',
                    '数据分析：指标定义 → 数据采集 → 分析方法 → 结论建议'
                ],
                'examples': [
                    '用户增长策略：通过A/B测试验证不同方案，优化注册转化率提升20%',
                    '需求优先级：采用RICE模型评估，聚焦高影响力、低投入的需求'
                ]
            },
            'data': {
                'keywords': ['SQL', '分析', '数据质量', '指标', '可视化', '建模', '清洗'],
                'templates': [
                    '分析流程：需求理解 → 数据获取 → 数据清洗 → 分析建模 → 结果呈现',
                    '指标体系：核心指标 → 辅助指标 → 监控告警 → 迭代优化',
                    '数据治理：数据标准 → 质量监控 → 安全合规 → 生命周期管理'
                ],
                'examples': [
                    '用户行为分析：通过漏斗分析定位流失环节，提出针对性优化方案',
                    '数据建模：采用回归分析预测用户留存，准确率达到85%'
                ]
            },
            'implementation': {
                'keywords': ['项目', '进度', '风险', '沟通', '部署', '培训', '交付'],
                'templates': [
                    '项目管理：目标设定 → 计划制定 → 执行监控 → 复盘总结',
                    '实施流程：需求确认 → 环境准备 → 系统部署 → 测试验收',
                    '客户管理：需求沟通 → 进度同步 → 问题解决 → 满意度跟踪'
                ],
                'examples': [
                    '项目风险管控：识别关键路径，制定应急预案，每周风险评审',
                    '客户沟通：定期进度汇报，及时响应问题，建立信任关系'
                ]
            }
        }
        
    def review(self, session_id: str) -> Dict[str, Any]:
        session_path = os.path.join(self.data_dir, f"interview_{session_id}.json")
        if not os.path.exists(session_path):
            raise ValueError("面试记录不存在")
        
        with open(session_path, 'r', encoding='utf-8') as f:
            session_data = json.load(f)
        
        position_type = session_data['position_type']
        criteria = self.evaluation_criteria.get(position_type, self.evaluation_criteria['dev'])
        
        professional_score = 0
        comprehensive_score = 0
        reviews = []
        
        for q in session_data['questions']:
            answer = session_data['answers'].get(q['id'], '')
            keyword_count = sum(1 for kw in criteria['keywords'] if kw in answer)
            length_score = min(len(answer) // 50, 3)
            
            question_review = {
                'question_id': q['id'],
                'question': q['question'],
                'answer': answer,
                'keyword_matches': [kw for kw in criteria['keywords'] if kw in answer],
                'score': min(keyword_count * 10 + length_score * 10, 100),
                'feedback': self._generate_feedback(q, answer, criteria)
            }
            reviews.append(question_review)
            
            professional_score += question_review['score']
            comprehensive_score += (keyword_count + length_score)
        
        professional_score = int(professional_score / len(session_data['questions']))
        comprehensive_score = int(min(comprehensive_score * 10, 100))
        
        return {
            'session_id': session_id,
            'professional_score': professional_score,
            'comprehensive_score': comprehensive_score,
            'reviews': reviews,
            'templates': criteria['templates'],
            'examples': criteria['examples']
        }
        
    def _generate_feedback(self, question, answer, criteria):
        if not answer:
            return '请提供更详细的回答'
        if len(answer) < 30:
            return '回答过于简短，建议补充更多细节'
        
        matched_kws = [kw for kw in criteria['keywords'] if kw in answer]
        if matched_kws:
            return f'回答中体现了{", ".join(matched_kws)}等关键点，建议进一步展开说明'
        return '回答基本完整，建议结合更多专业术语和方法论'
