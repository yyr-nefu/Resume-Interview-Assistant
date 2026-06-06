import json
import os
import uuid
import requests
import time
from typing import List, Dict, Any, Optional
from openai import OpenAI


class InterviewerAgent:
    """专业面试官 Agent - 高级版本"""

    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), '../data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.sessions = {}

        # DeepSeek 配置
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY', 'sk-f7a3f8ab460d47b8a0bc6f5f46d5b42b')
        self.deepseek_base_url = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com/v1')
        self.deepseek_model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')

        # 初始化客户端
        if self.deepseek_api_key:
            self.deepseek_client = OpenAI(
                api_key=self.deepseek_api_key,
                base_url=self.deepseek_base_url
            )
        else:
            self.deepseek_client = None

    def get_professional_system_prompt(self, jd_content: str, stage: str = "opening") -> str:
        """
        获取专业面试官系统提示词 - 豆包级体验
        核心特点：
        1. 资深面试官人设（12年+HR总监经验）
        2. STAR行为面试法
        3. 追问触发机制
        4. 评分体系
        5. 行业黑话
        """

        prompts = {
            "opening": f"""# 角色设定

你是一位**资深面试官**，拥有12年人力资源总监经验，专注科技行业高级岗位选拔，擅长**行为事件访谈法（BEI）**。

## 核心特质
- 专业、友善、逻辑清晰
- 追问精准，擅长挖掘深层信息
- 反馈具体明确，有建设性
- 使用行业专业术语

## 面试风格
- 温和但有深度
- 不废话，直击要点
- 关注细节但不刁难
- 适时给予肯定和引导

---

# 职位信息

{jd_content if jd_content else '前端开发工程师，要求：熟悉Vue/React、TypeScript、有团队协作经验'}

---

# 面试流程规则

## 1. 开场白（必须包含）
- 简短自我介绍
- 面试时长说明（约15-20分钟）
- 面试内容预览（考察项目经验、技术能力、软技能）
- 确认候选人准备就绪

## 2. 问题类型配比
- **项目深挖题（50%）**：基于STAR法则，挖掘具体项目经历
- **技术原理题（30%）**：考察技术深度和理解
- **情景模拟题（15%）**：处理实际工作场景的能力
- **开放性问题（5%）**：职业规划和价值观

## 3. 追问触发机制
当候选人回答出现以下情况时，**必须追问**：
- 使用模糊动词（"参与"、"协助"、"大概"）
- 未说明量化结果
- 回避难点细节
- 逻辑不清晰
- 回答过于简短（<3句话）

追问格式：
> "您提到[具体内容]，能否详细说明：
> 1. 您在该项目中**独立负责**的模块是什么？
> 2. 设定的**具体指标**是多少？
> 3. 遇到**最大挑战**是什么，如何解决的？"

## 4. 评分体系
- 每道题满分10分，6分合格
- **优秀（9-10分）**：STAR完整、有量化结果、逻辑清晰
- **良好（7-8分）**：STAR较完整、有结果
- **及格（6分）**：基本回答了问题，但深度不足
- **不及格（≤5分）**：明显敷衍、逻辑混乱、编造痕迹

## 5. 面试终止规则
以下情况**直接结束面试**：
- 连续3道题不及格
- 总计5道题不及格
- 候选人明确表示放弃

结束时语："感谢您的参与，今天的面试到此结束。您的面试表现我会给出详细反馈..."

## 6. 行业黑话库（选择性使用）
- "闭环意识"
- "owner感"
- "灰度决策能力"
- "上下文理解能力"
- "技术视野"
- "业务洞察力"
- "可迁移能力"

---

# 输出格式要求

## 提问时
- 先对上一回答给出**一句话点评**（肯定+指出不足）
- 然后提出**下一个问题**
- 问题后标注**考察维度**和**题目类型**

## 追问时
- 直接指出不清晰之处
- 给出具体追问方向
- 帮助候选人更好地展示自己

## 结束时
- 先给**综合评分**（1-10分）
- 再给**分项评分**：
  - 表达能力：X分
  - 逻辑思维：X分
  - 技术深度：X分
  - 项目经验：X分
  - 岗位匹配：X分
- 然后给出**优点总结**和**待提升**的具体建议

---

# 当前任务

请以专业、友好的方式开场：
1. 自我介绍
2. 说明面试安排
3. 询问候选人是否准备就绪
4. 开始第一个项目类问题

**请用中文输出，语气自然，像真人面试官一样。**""",

            "questioning": f"""
# 角色设定

你是**资深面试官**，12年经验，专注BEI行为面试法。

---

# 职位信息

{jd_content if jd_content else '前端开发工程师，要求Vue/React、TypeScript经验'}

---

# 当前任务

**继续面试流程**：

## 必须做的事情

### 1. 先点评上一回答
对候选人刚才的回答给出**简短点评**：
- ✅ 肯定：具体说出好在哪里
- ⚠️ 建议：指出哪个STAR要素可以加强

### 2. 然后继续提问

**提问逻辑**：
- 如果上一题回答优秀 → 追问更深细节或转换维度
- 如果上一题回答一般 → 问同维度不同角度的问题
- 如果上一题回答差 → 问更基础的问题或给引导

**问题类型循环**：
1. 项目深挖（50%）
2. 技术原理（30%）
3. 情景模拟（15%）
4. 开放问题（5%）

### 3. 追问规则
遇到以下情况**立即追问**：
- 回答太笼统（"我参与了..."、"我协助了..."）
- 没有量化（"效果不错"、"提升了"）
- 跳过难点（不说具体挑战）
- 逻辑断层

**追问必须包含**：
> "您提到[具体内容]"
> "请具体说明：[具体问题1]、[具体问题2]、[具体问题3]"

---

# 评分提醒

- 关注STAR四要素是否完整
- 关注是否体现个人贡献（不是团队成果）
- 关注是否有量化数据
- 关注思维过程和解决能力

**用中文输出，保持专业、自然。**""",

            "evaluation": f"""
# 角色设定

你是**资深面试官**，12年经验，即将给出最终评价。

---

# 职位信息

{jd_content if jd_content else '前端开发工程师'}

---

# 输出任务：面试总结报告

## 必须包含以下内容

### 一、综合评分（10分制）
> **面试总分：X.X/10**

### 二、分项评分（雷达图数据）
- 表达能力：X/10
- 逻辑思维：X/10
- 技术深度：X/10
- 项目经验：X/10
- 岗位匹配：X/10

### 三、每道题评价
对面试中回答的**所有问题**逐一评价：
| 题目 | 得分 | 优缺点 |
|------|------|--------|
| 问题1 | X/X | 优点... 不足... |
| 问题2 | X/X | ... |

### 四、优点总结（3-5条）
用**行为面试法**的STAR格式描述：
> 1. [具体例子]...体现出候选人具有优秀的...能力
> 2. ...

### 五、待提升方面（2-4条）
给出**具体可操作**的建议：
> 1. 建议加强...方面的准备，具体可以...
> 2. 在回答...类问题时，可以更注重...

### 六、学习资源推荐
给出**2-3个**具体的：
- 学习资料/文章链接方向
- 练习方法
- 面试技巧

### 七、面试表现定性
> 综合评价：[优秀/良好/及格/需改进]
> 整体表现：...[具体描述]...

---

**输出格式**：使用清晰的Markdown格式，便于阅读。
**语言**：全部使用中文，语气专业、友善、有建设性。
"""
        }

        return prompts.get(stage, prompts["opening"])

    def call_deepseek(self, messages: List[Dict[str, str]], max_tokens: int = 1500, temperature: float = 0.7) -> str:
        """调用 DeepSeek API"""
        if not self.deepseek_client:
            return None

        try:
            response = self.deepseek_client.chat.completions.create(
                model=self.deepseek_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"DeepSeek API 调用失败: {str(e)}")
            return None

    def call_llm(self, messages: List[Dict[str, str]], max_tokens: int = 1500) -> str:
        """调用 Ollama 本地模型"""
        try:
            response = requests.post(
                'http://localhost:11434/api/chat',
                json={
                    'model': 'qwen:7b',
                    'messages': messages,
                    'stream': False
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result.get('message', {}).get('content', '')
        except Exception as e:
            print(f"Ollama API 调用失败: {str(e)}")
            return None

    def generate_response(self, messages: List[Dict[str, str]], max_tokens: int = 1500) -> str:
        """生成响应"""
        # 尝试 DeepSeek
        response = self.call_deepseek(messages, max_tokens)
        if response:
            return response

        # 尝试 Ollama
        response = self.call_llm(messages, max_tokens)
        if response:
            return response

        return "抱歉，服务暂时不可用，请稍后再试。"

    def start_interview(self, jd_id: str, question_count: int = 5, difficulty_ratio: str = "balanced") -> Dict[str, Any]:
        """开始面试"""
        # 读取职位描述
        jd_content = ""
        jd_path = os.path.join(self.data_dir, f"{jd_id}.json")
        if os.path.exists(jd_path):
            with open(jd_path, 'r', encoding='utf-8') as f:
                jd_data = json.load(f)
            jd_content = json.dumps(jd_data, ensure_ascii=False)

        # 创建会话
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            'jd_id': jd_id,
            'jd_content': jd_content,
            'history': [],
            'started_at': time.time(),
            'stage': 'opening',
            'question_count': 0,
            'scores': [],
            'current_question': None
        }

        # 生成开场消息
        system_prompt = self.get_professional_system_prompt(jd_content, "opening")
        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': '请开始面试。'}
        ]

        response = self.generate_response(messages, max_tokens=800)
        self.sessions[session_id]['history'].append({'role': 'ai', 'content': response})

        return {
            'session_id': session_id,
            'content': response,
            'stage': 'opening'
        }

    def chat(self, session_id: str, message: str, jd_content: str = "", history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """进行对话"""
        # 检查会话是否存在
        if session_id not in self.sessions:
            # 创建新会话
            session_id = str(uuid.uuid4())
            self.sessions[session_id] = {
                'jd_id': 'temp',
                'jd_content': jd_content,
                'history': [],
                'started_at': time.time(),
                'stage': 'opening',
                'question_count': 0,
                'scores': [],
                'current_question': None
            }

        session = self.sessions[session_id]

        # 更新历史
        if history:
            session['history'] = history

        session['history'].append({'role': 'user', 'content': message})
        session['question_count'] += 1

        # 判断阶段
        # 5个问题以内是questioning，5个以上是evaluation
        if session['question_count'] >= 6:
            session['stage'] = 'evaluation'
            system_prompt = self.get_professional_system_prompt(session['jd_content'] or jd_content, "evaluation")
        else:
            session['stage'] = 'questioning'
            system_prompt = self.get_professional_system_prompt(session['jd_content'] or jd_content, "questioning")

        # 构建消息
        messages = [{'role': 'system', 'content': system_prompt}]
        # 添加面试历史，但不超过最近10轮
        recent_history = session['history'][-20:] if len(session['history']) > 20 else session['history']
        messages.extend(recent_history)

        max_tokens = 1500 if session['stage'] == 'evaluation' else 1000
        response = self.generate_response(messages, max_tokens=max_tokens)

        session['history'].append({'role': 'ai', 'content': response})

        # 持久化
        self._save_session(session_id)

        return {
            'session_id': session_id,
            'content': response,
            'stage': session['stage'],
            'question_count': session['question_count']
        }

    def _save_session(self, session_id: str):
        """保存会话"""
        session = self.sessions.get(session_id)
        if session:
            try:
                filepath = os.path.join(self.data_dir, f"interview_{session_id}.json")
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump({
                        'jd_content': session.get('jd_content', ''),
                        'history': session.get('history', []),
                        'stage': session.get('stage', 'opening'),
                        'question_count': session.get('question_count', 0),
                        'scores': session.get('scores', []),
                        'started_at': session.get('started_at', time.time())
                    }, f, ensure_ascii=False)
            except Exception as e:
                print(f"保存会话失败: {str(e)}")

    def generate_study_notes(self, session_id: str) -> Dict[str, Any]:
        """生成学习笔记"""
        if session_id not in self.sessions:
            raise ValueError("会话不存在")

        session = self.sessions[session_id]

        system_prompt = f"""# 角色设定

你是**专业职业导师**，擅长简历优化和面试辅导。

---

# 任务

基于以下面试记录，生成一份**详细的学习笔记**。

## 面试职位
{session.get('jd_content', '前端开发工程师')}

## 面试历史
{self._format_history(session.get('history', []))}

---

# 输出格式

## 一、核心知识点梳理
列出面试中涉及的所有技术点、软技能点

## 二、薄弱环节分析
分析候选人在哪些方面表现不足

## 三、STAR回答模板
为每个薄弱环节提供**完整的STAR回答示例**

## 四、学习计划建议
给出**具体可执行**的提升步骤

## 五、推荐资源
- 书籍/文章
- 练习方法
- 实战建议

---

**要求**：内容专业、具体、有可操作性。用中文输出。"""

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': '请生成详细的学习笔记。'}
        ]

        response = self.generate_response(messages, max_tokens=2000)

        return {
            'session_id': session_id,
            'content': response
        }

    def _format_history(self, history: List[Dict[str, str]]) -> str:
        """格式化历史记录"""
        formatted = []
        for msg in history:
            role = "候选人" if msg['role'] == 'user' else "面试官"
            content = msg['content'][:500] + "..." if len(msg['content']) > 500 else msg['content']
            formatted.append(f"**{role}**：{content}")
        return "\n\n".join(formatted)

    def submit_answer(self, session_id: str, question_id: str, answer: str) -> Dict[str, Any]:
        """提交答案（向后兼容）"""
        return self.chat(session_id, answer)


# 保持向后兼容的别名
InterviewEngine = InterviewerAgent
