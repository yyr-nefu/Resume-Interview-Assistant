<template>
  <div class="interview-container">
    <div class="interview-header">
      <div class="header-left">
        <div class="header-icon">
          <Message />
        </div>
        <div class="header-text">
          <h2>AI模拟面试</h2>
          <p>基于JD智能生成面试问题</p>
        </div>
      </div>
      <div class="header-right">
        <el-button @click="clearHistory" class="action-btn">
          <Delete />
          清空对话
        </el-button>
        <el-button type="primary" @click="goToNotes" class="action-btn primary">
          <Memo />
          学习笔记
        </el-button>
      </div>
    </div>
    
    <div class="chat-container" ref="chatContainer">
      <div class="welcome-message" v-if="messages.length === 0">
        <div class="welcome-icon">
          <ChatDotRound :size="72" />
        </div>
        <h3>准备开始面试</h3>
        <p>AI面试官将根据JD内容向你提问</p>
        <el-button type="primary" size="large" @click="startInterview" class="start-btn">
          <VideoPlay />
          开始面试
        </el-button>
      </div>
      
      <div class="message-list">
        <div 
          v-for="(msg, index) in messages" 
          :key="index"
          :class="['message', msg.role]"
        >
          <div class="message-avatar">
            <el-avatar v-if="msg.role === 'ai'" :size="40" class="ai-avatar">
              <ChatDotRound />
            </el-avatar>
            <el-avatar v-else :size="40" class="user-avatar">
              <User />
            </el-avatar>
          </div>
          <div class="message-content">
            <div class="message-bubble" v-html="formatMessage(msg.content)"></div>
            <div class="message-actions" v-if="msg.role === 'user' && msg.id">
              <el-button 
                size="small" 
                text 
                @click="collectAnswer(msg)"
                :class="{ 'collected': msg.collected }"
              >
                <Star v-if="!msg.collected" />
                <StarFilled v-else />
                {{ msg.collected ? '已收藏' : '收藏回答' }}
              </el-button>
            </div>
          </div>
        </div>
        
        <div class="message ai typing" v-if="isTyping">
          <div class="message-avatar">
            <el-avatar :size="40" class="ai-avatar">
              <ChatDotRound />
            </el-avatar>
          </div>
          <div class="message-content">
            <div class="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="input-area">
      <div class="input-wrapper">
        <el-input
          v-model="userInput"
          type="textarea"
          :rows="2"
          placeholder="输入你的回答..."
          :disabled="!isInterviewActive"
          @keydown.enter.ctrl="sendMessage"
          class="message-input"
        />
        <div class="input-actions">
          <span class="hint">Ctrl + Enter 发送</span>
          <el-button 
            type="primary" 
            :disabled="!isInterviewActive || !userInput.trim()"
            @click="sendMessage"
            class="send-btn"
          >
            <Promotion />
            发送
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  ChatDotRound, User, VideoPlay, Memo, Star, StarFilled, 
  Message, Delete, Promotion 
} from '@element-plus/icons-vue'

const router = useRouter()

const messages = ref([])
const userInput = ref('')
const isTyping = ref(false)
const isInterviewActive = ref(false)
const currentQuestionIndex = ref(0)
const chatContainer = ref(null)

const questions = [
  "请做一个简单的自我介绍，重点介绍与这个岗位相关的经历。",
  "你为什么对这个岗位感兴趣？你对这个行业有什么了解？",
  "请描述一下你最近完成的一个项目，你在其中扮演什么角色？",
  "你遇到过的最大挑战是什么？你是如何解决的？",
  "对于团队合作，你有什么经验可以分享？",
]

const scrollToBottom = () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

const formatMessage = (content) => {
  return content.replace(/\n/g, '<br>')
}

const startInterview = () => {
  const jdContent = localStorage.getItem('jdContent')
  if (!jdContent) {
    ElMessage.warning('请先在首页填写JD内容')
    router.push('/')
    return
  }
  
  isInterviewActive.value = true
  messages.value = []
  currentQuestionIndex.value = 0
  
  const intro = `你好！我是AI面试官，我会根据你提供的岗位要求向你提问。

**岗位要求分析：**
- 技术能力：需要具备相关技术栈
- 软技能：沟通能力、团队协作
- 综合素质：学习能力、问题解决能力

准备好了吗？我们开始吧！`

  messages.value.push({
    role: 'ai',
    content: intro
  })
  
  setTimeout(() => {
    askQuestion()
  }, 1000)
}

const askQuestion = () => {
  if (currentQuestionIndex.value >= questions.length) {
    const endMessage = `
**面试结束！**

感谢你的参与，以下是一些建议：

📚 **学习建议**：
1. 回顾刚才的回答，思考如何改进
2. 查看学习笔记，系统性复习知识点
3. 收藏你满意的回答，作为面试素材

💡 **下一步**：
- 生成个性化学习笔记
- 查看收藏的回答
- 再次练习或优化简历
`
    messages.value.push({
      role: 'ai',
      content: endMessage
    })
    isInterviewActive.value = false
    return
  }
  
  const question = questions[currentQuestionIndex.value]
  messages.value.push({
    role: 'ai',
    content: `**第 ${currentQuestionIndex.value + 1} 题**\n\n${question}`
  })
  scrollToBottom()
}

const sendMessage = () => {
  if (!userInput.value.trim()) return
  
  const userMessage = {
    role: 'user',
    content: userInput.value,
    id: `msg_${Date.now()}`,
    collected: false
  }
  
  messages.value.push(userMessage)
  userInput.value = ''
  scrollToBottom()
  
  isTyping.value = true
  
  setTimeout(() => {
    isTyping.value = false
    
    const responses = [
      '感谢你的回答！回答得不错，让我继续下一个问题。',
      '明白了，你的回答很有见地。我们继续。',
      '好的，我理解你的意思了。下一个问题。',
      '收到！你的经验很丰富。接下来...',
      '回答得很好！让我们继续下一道题。',
    ]
    
    const response = responses[Math.floor(Math.random() * responses.length)]
    messages.value.push({
      role: 'ai',
      content: response
    })
    
    currentQuestionIndex.value++
    
    setTimeout(() => {
      askQuestion()
    }, 1500)
    
    scrollToBottom()
  }, 1000)
}

const collectAnswer = (msg) => {
  msg.collected = !msg.collected
  
  if (msg.collected) {
    const favorites = JSON.parse(localStorage.getItem('favorites') || '[]')
    favorites.push({
      id: msg.id,
      question: getLastQuestion(),
      answer: msg.content,
      createdAt: new Date().toISOString()
    })
    localStorage.setItem('favorites', JSON.stringify(favorites))
    ElMessage.success('已收藏到收藏夹')
  } else {
    ElMessage.info('已取消收藏')
  }
}

const getLastQuestion = () => {
  const userMessages = messages.value.filter(m => m.role === 'user')
  if (userMessages.length > 1) {
    const lastAIMessages = messages.value.filter(m => m.role === 'ai')
    for (let i = lastAIMessages.length - 1; i >= 0; i--) {
      if (lastAIMessages[i].content.includes('**第')) {
        return lastAIMessages[i].content.replace(/<[^>]*>/g, '').split('\n\n')[1] || ''
      }
    }
  }
  return ''
}

const clearHistory = () => {
  messages.value = []
  isInterviewActive.value = false
  currentQuestionIndex.value = 0
  localStorage.removeItem('interviewMessages')
}

const goToNotes = () => {
  router.push('/notes')
}

onMounted(() => {
  const savedMessages = localStorage.getItem('interviewMessages')
  if (savedMessages) {
    messages.value = JSON.parse(savedMessages)
    isInterviewActive.value = true
  }
})

import { watch } from 'vue'
watch(messages, (newMessages) => {
  if (newMessages.length > 0) {
    localStorage.setItem('interviewMessages', JSON.stringify(newMessages))
  }
}, { deep: true })
</script>

<style scoped>
.interview-container {
  max-width: 950px;
  margin: 0 auto;
  height: calc(100vh - 140px);
  display: flex;
  flex-direction: column;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.interview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 32px;
  background: linear-gradient(135deg, #f8f9fa 0%, #f3f4f6 100%);
  border-bottom: 1px solid #e5e7eb;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
}

.header-icon .el-icon {
  font-size: 24px;
  color: #ffffff;
}

.header-text h2 {
  font-size: 22px;
  font-weight: 700;
  color: #1d1d1f;
  margin: 0 0 4px 0;
}

.header-text p {
  font-size: 14px;
  color: #6b7280;
  margin: 0;
}

.header-right {
  display: flex;
  gap: 12px;
}

.action-btn {
  padding: 10px 20px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.25s ease;
}

.action-btn:hover {
  transform: translateY(-1px);
}

.action-btn.primary {
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(0, 122, 255, 0.3);
}

.action-btn.primary:hover {
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 24px 32px;
  background: #fafafa;
}

.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

.welcome-message {
  text-align: center;
  padding: 80px 32px;
}

.welcome-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.1) 0%, rgba(88, 86, 214, 0.1) 100%);
  border-radius: 32px;
  color: #007aff;
}

.welcome-message h3 {
  font-size: 26px;
  color: #1d1d1f;
  margin-bottom: 12px;
  font-weight: 600;
}

.welcome-message p {
  color: #6b7280;
  margin-bottom: 40px;
  font-size: 15px;
}

.start-btn {
  padding: 16px 40px;
  border-radius: 16px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  border: none;
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.35);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.start-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0, 122, 255, 0.45);
}

.message-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.message {
  display: flex;
  gap: 14px;
  animation: fadeInUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.message.ai {
  justify-content: flex-start;
}

.message.user {
  justify-content: flex-end;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-avatar {
  flex-shrink: 0;
}

.ai-avatar {
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.3);
}

.user-avatar {
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 70%;
}

.message-bubble {
  padding: 18px 22px;
  border-radius: 24px;
  line-height: 1.7;
  font-size: 15px;
  position: relative;
}

.message.ai .message-bubble {
  background: #ffffff;
  color: #1d1d1f;
  border-bottom-left-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.message.user .message-bubble {
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  color: white;
  border-bottom-right-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 122, 255, 0.25);
}

.message-bubble :deep(p) {
  margin: 0 0 8px 0;
}

.message-bubble :deep(p:last-child) {
  margin-bottom: 0;
}

.message-bubble :deep(strong) {
  font-weight: 600;
}

.message-bubble :deep(ul),
.message-bubble :deep(ol) {
  padding-left: 20px;
  margin: 8px 0;
}

.message-bubble :deep(li) {
  margin-bottom: 6px;
}

.message-actions {
  display: flex;
  gap: 10px;
}

.message-actions .el-button {
  padding: 6px 14px;
  font-size: 13px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.message-actions .collected {
  color: #f59e0b;
}

.message-actions .collected:hover {
  background: rgba(245, 158, 11, 0.1);
}

.typing-indicator {
  display: flex;
  gap: 6px;
  padding: 18px 22px;
  background: #ffffff;
  border-radius: 24px;
  border-bottom-left-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.typing-indicator span {
  width: 10px;
  height: 10px;
  background: #9ca3af;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(1) {
  animation-delay: 0s;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0.7);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.input-area {
  padding: 20px 32px;
  background: #ffffff;
  border-top: 1px solid #e5e7eb;
}

.input-wrapper {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.message-input :deep(.el-textarea) {
  border-radius: 20px;
  overflow: hidden;
}

.message-input :deep(.el-textarea__inner) {
  border-radius: 20px;
  border: 2px solid #e5e7eb;
  padding: 16px 20px;
  font-size: 15px;
  resize: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  min-height: 60px;
  max-height: 120px;
}

.message-input :deep(.el-textarea__inner:focus) {
  border-color: #007aff;
  box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
}

.message-input :deep(.el-textarea__inner:disabled) {
  background: #f9fafb;
  cursor: not-allowed;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hint {
  font-size: 13px;
  color: #9ca3af;
}

.send-btn {
  padding: 14px 32px;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 600;
  background: linear-gradient(135deg, #007aff 0%, #5856d6 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(0, 122, 255, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.send-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
}

.send-btn:disabled {
  background: #d1d5db;
  box-shadow: none;
}

@media (max-width: 768px) {
  .interview-container {
    height: calc(100vh - 120px);
    border-radius: 0;
    box-shadow: none;
  }
  
  .interview-header {
    padding: 16px 20px;
  }
  
  .header-icon {
    width: 40px;
    height: 40px;
  }
  
  .header-icon .el-icon {
    font-size: 20px;
  }
  
  .header-text h2 {
    font-size: 18px;
  }
  
  .action-btn {
    padding: 8px 14px;
    font-size: 12px;
  }
  
  .chat-container {
    padding: 16px 20px;
  }
  
  .welcome-message {
    padding: 60px 20px;
  }
  
  .welcome-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 20px;
  }
  
  .welcome-message h3 {
    font-size: 22px;
  }
  
  .message-content {
    max-width: 85%;
  }
  
  .message-bubble {
    padding: 14px 18px;
    font-size: 14px;
  }
  
  .input-area {
    padding: 16px 20px;
  }
  
  .send-btn {
    padding: 12px 24px;
    font-size: 14px;
  }
}
</style>
