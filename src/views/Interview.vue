<template>
  <div class="interview-page min-h-screen">
    <div class="max-w-6xl mx-auto px-8 py-12">
      <!-- Header -->
      <div class="flex items-center justify-between mb-12">
        <div class="flex items-center gap-6">
          <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-2xl shadow-blue-500/40">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <div>
            <h1 class="text-3xl font-bold text-white">模拟面试</h1>
            <p class="text-slate-400 text-base">AI 面试官 - 专业面试辅导</p>
          </div>
        </div>
        
        <div class="flex items-center gap-4">
          <button 
            v-if="messages.length > 0 && !isGeneratingStudyNotes"
            @click="generateStudyNotes"
            :disabled="isGeneratingStudyNotes"
            class="px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-xl text-white font-semibold hover:shadow-xl hover:shadow-emerald-500/40 hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <span>生成学习笔记</span>
          </button>
          <button 
            @click="clearMessages"
            class="px-6 py-3 bg-white/5 border border-white/10 rounded-xl text-slate-300 hover:text-white hover:bg-white/10 hover:border-white/20 transition-all duration-300 flex items-center gap-3"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            <span>清空</span>
          </button>
          <router-link 
            to="/notes"
            class="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl text-white font-semibold hover:shadow-xl hover:shadow-blue-500/40 hover:scale-[1.02] transition-all duration-300 flex items-center gap-3"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            <span>学习笔记</span>
          </router-link>
        </div>
      </div>

      <!-- Messages Container -->
      <div class="bg-gradient-to-br from-white/5 to-white/0 border border-white/10 rounded-[3rem] overflow-hidden shadow-2xl shadow-blue-500/20">
        <div class="h-[600px] overflow-y-auto p-10 space-y-6" ref="messagesContainer">
          <!-- Welcome State -->
          <div v-if="messages.length === 0 && !isGeneratingStudyNotes" class="flex flex-col items-center justify-center h-full text-center space-y-8">
            <div class="space-y-4">
              <h2 class="text-4xl font-bold text-white">准备好面试了吗？</h2>
              <p class="text-xl text-slate-400 max-w-2xl leading-relaxed">
                AI 面试官会根据您的职位描述进行专业面试，给出评价和建议。
              </p>
            </div>
            
            <!-- JD Input -->
            <div class="w-full max-w-3xl space-y-6">
              <div class="text-left">
                <label class="flex items-center gap-3 text-white font-semibold text-lg mb-3">
                  <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  岗位描述（可选）
                </label>
                <textarea 
                  v-model="jdContent"
                  placeholder="请粘贴目标岗位的职位描述（JD），AI 面试官将根据此进行针对性提问..."
                  class="w-full h-40 bg-slate-900/50 border-2 border-white/10 rounded-2xl px-6 py-5 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/30 transition-all resize-none text-base leading-relaxed"
                />
              </div>
              
              <!-- Quick Templates -->
              <div class="text-left">
                <p class="text-slate-500 text-sm mb-3 font-medium">快速模板：</p>
                <div class="flex flex-wrap gap-3">
                  <button 
                    @click="useTemplate('frontend')"
                    class="px-5 py-2.5 bg-white/5 border border-white/10 rounded-xl text-slate-300 text-sm font-medium hover:text-white hover:bg-white/10 hover:border-white/20 hover:scale-[1.02] transition-all"
                  >
                    前端开发
                  </button>
                  <button 
                    @click="useTemplate('backend')"
                    class="px-5 py-2.5 bg-white/5 border border-white/10 rounded-xl text-slate-300 text-sm font-medium hover:text-white hover:bg-white/10 hover:border-white/20 hover:scale-[1.02] transition-all"
                  >
                    后端开发
                  </button>
                  <button 
                    @click="useTemplate('product')"
                    class="px-5 py-2.5 bg-white/5 border border-white/10 rounded-xl text-slate-300 text-sm font-medium hover:text-white hover:bg-white/10 hover:border-white/20 hover:scale-[1.02] transition-all"
                  >
                    产品经理
                  </button>
                </div>
              </div>
            </div>
            
            <button 
              @click="startInterview"
              :disabled="isGenerating"
              class="px-12 py-5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl text-white font-bold text-xl shadow-xl shadow-blue-500/40 hover:shadow-2xl hover:shadow-blue-500/60 hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center gap-3"
            >
              <svg v-if="isGenerating" class="w-7 h-7 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ isGenerating ? '正在准备面试...' : '开始面试' }}</span>
            </button>
          </div>

          <!-- Study Notes State -->
          <div v-else-if="isGeneratingStudyNotes || studyNotes" class="flex flex-col items-center justify-start h-full space-y-8">
            <div v-if="isGeneratingStudyNotes" class="flex flex-col items-center justify-center h-full space-y-6">
              <div class="w-20 h-20 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 rounded-3xl flex items-center justify-center">
                <svg class="w-10 h-10 text-emerald-400 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </div>
              <p class="text-white text-2xl font-semibold">正在生成学习笔记...</p>
            </div>
            
            <div v-else class="w-full">
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-2xl font-bold text-white flex items-center gap-3">
                  <svg class="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  学习笔记
                </h3>
                <button 
                  @click="saveToNotes"
                  class="px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-600 rounded-xl text-white font-semibold hover:shadow-xl hover:shadow-emerald-500/40 hover:scale-[1.02] transition-all duration-300 flex items-center gap-3"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  <span>保存到笔记</span>
                </button>
              </div>
              <div class="bg-white/5 border border-white/10 rounded-2xl p-8 max-h-[400px] overflow-y-auto">
                <pre class="text-white whitespace-pre-wrap font-sans text-base leading-relaxed">{{ studyNotes }}</pre>
              </div>
              <button 
                @click="resetToInterview"
                class="mt-6 px-8 py-4 bg-white/5 border border-white/10 rounded-xl text-white font-semibold hover:bg-white/10 hover:border-white/20 transition-all duration-300 w-full text-lg"
              >
                返回面试
              </button>
            </div>
          </div>

          <!-- Messages -->
          <div v-else>
            <div v-for="message in messages" :key="message.id" class="flex gap-5">
              <!-- AI Message -->
              <div v-if="message.role === 'ai'" class="flex items-start gap-5 w-full">
                <div class="flex-shrink-0 w-14 h-14 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center shadow-xl shadow-blue-500/30">
                  <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <div class="bg-gradient-to-br from-white/10 to-white/5 border border-white/10 rounded-3xl rounded-tl-none p-6 max-w-[85%]">
                    <p class="text-white text-base leading-relaxed whitespace-pre-wrap">{{ message.content }}</p>
                  </div>
                  <div class="flex items-center gap-3 mt-3">
                    <button 
                      @click="toggleCollection(message)"
                      :class="[
                        'px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-300 flex items-center gap-2',
                        message.collected 
                          ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' 
                          : 'text-slate-400 hover:text-white hover:bg-white/5'
                      ]"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                      </svg>
                      <span>{{ message.collected ? '已保存' : '保存' }}</span>
                    </button>
                  </div>
                </div>
              </div>

              <!-- User Message -->
              <div v-else class="flex items-start gap-5 w-full justify-end">
                <div class="flex-1 text-right">
                  <div class="bg-gradient-to-br from-blue-500/30 to-purple-600/30 border border-blue-500/30 rounded-3xl rounded-tr-none p-6 max-w-[85%] ml-auto">
                    <p class="text-white text-base leading-relaxed whitespace-pre-wrap">{{ message.content }}</p>
                  </div>
                </div>
                <div class="flex-shrink-0 w-14 h-14 bg-gradient-to-br from-emerald-500 to-teal-500 rounded-2xl flex items-center justify-center shadow-xl shadow-emerald-500/30">
                  <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Input Area -->
        <div v-if="messages.length > 0 && !isGeneratingStudyNotes && !studyNotes" class="border-t border-white/10 p-8 bg-slate-900/50">
          <form @submit.prevent="sendMessage" class="flex gap-4">
            <input 
              v-model="inputMessage"
              :disabled="isGenerating"
              type="text"
              placeholder="输入您的回答..."
              class="flex-1 bg-slate-900/50 border-2 border-white/10 rounded-2xl px-6 py-5 text-white text-base placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/30 transition-all disabled:opacity-50"
            >
            <button 
              type="submit"
              :disabled="!inputMessage.trim() || isGenerating"
              class="px-8 py-5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl text-white font-semibold text-base hover:shadow-xl hover:shadow-blue-500/40 hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center gap-3"
            >
              <svg v-if="isGenerating" class="w-6 h-6 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
              <span>{{ isGenerating ? '思考中...' : '发送' }}</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import { api } from '@/utils/api'

const router = useRouter()
const appStore = useAppStore()

const messagesContainer = ref<HTMLElement | null>(null)
const messages = ref<Array<{ id: string, role: 'user' | 'ai', content: string, collected?: boolean }>>([])
const inputMessage = ref('')
const isGenerating = ref(false)
const isGeneratingStudyNotes = ref(false)
const studyNotes = ref<string | null>(null)
const sessionId = ref<string | null>(null)
const jdContent = ref('')

const templates = {
  frontend: `前端开发工程师

职责要求：
- 负责公司产品的前端开发工作，使用 Vue/React 等主流框架
- 参与前端架构设计和技术选型
- 优化前端性能，提升用户体验
- 与产品和设计团队紧密配合

技能要求：
- 熟练掌握 HTML/CSS/JavaScript
- 熟悉 Vue 或 React 框架
- 了解前端工程化和构建工具（Webpack/Vite）
- 有良好的代码规范和团队协作能力`,
  
  backend: `后端开发工程师

职责要求：
- 负责服务端业务逻辑开发
- 设计并实现高并发、高可用的系统架构
- 优化数据库性能和系统稳定性
- 编写技术文档和代码规范

技能要求：
- 熟练掌握 Python/Go/Java 等后端语言
- 熟悉 MySQL/Redis/MongoDB 等数据库
- 了解微服务架构和容器化部署
- 有大型项目开发经验优先`,
  
  product: `产品经理

职责要求：
- 负责产品规划和功能设计
- 收集和分析用户需求，撰写 PRD
- 协调研发、设计、测试团队推进项目
- 跟踪产品数据，持续优化产品体验

技能要求：
- 具备良好的产品思维和用户视角
- 熟悉产品设计和项目管理流程
- 优秀的沟通表达和跨部门协作能力
- 有互联网产品经验优先`
}

function useTemplate(type: 'frontend' | 'backend' | 'product') {
  jdContent.value = templates[type]
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

async function startInterview() {
  isGenerating.value = true
  
  try {
    const jd = jdContent.value || appStore.jdContent || '前端开发工程师职位，要求熟悉Vue、React等框架，有团队协作经验。'
    
    const response = await api.post('/api/interview/chat', {
      message: '开始面试',
      session_id: null,
      context: {
        jd: jd
      }
    })
    
    sessionId.value = response.session_id
    
    messages.value.push({
      id: `ai-${Date.now()}`,
      role: 'ai',
      content: response.content
    })
  } catch (error) {
    messages.value.push({
      id: `ai-${Date.now()}`,
      role: 'ai',
      content: '您好！我是您的 AI 面试官。让我们开始今天的面试。\n\n请先简单介绍一下您自己，包括您的工作背景和项目经验。'
    })
  } finally {
    isGenerating.value = false
    scrollToBottom()
  }
}

async function sendMessage() {
  if (!inputMessage.value.trim() || isGenerating.value) return
  
  const userContent = inputMessage.value.trim()
  inputMessage.value = ''
  
  messages.value.push({
    id: `user-${Date.now()}`,
    role: 'user',
    content: userContent
  })
  scrollToBottom()
  
  isGenerating.value = true
  
  try {
    const jd = jdContent.value || appStore.jdContent || ''
    
    const response = await api.post('/api/interview/chat', {
      message: userContent,
      session_id: sessionId.value,
      context: {
        jd: jd,
        history: messages.value.slice(0, -1).map(m => ({
          role: m.role,
          content: m.content
        }))
      }
    })
    
    sessionId.value = response.session_id
    
    messages.value.push({
      id: `ai-${Date.now()}`,
      role: 'ai',
      content: response.content
    })
  } catch (error) {
    const fallbackResponses = [
      '感谢您的回答！这个回答展示了您对技术的理解。接下来的问题是：\n\n能否分享一个您在项目中遇到的技术挑战，以及您是如何解决的？',
      '很好！我能看出您在这个方面有一定的经验。让我们继续下一个话题：\n\n您对团队协作有什么看法？请分享一个团队项目的经验。',
      '非常感谢您的分享！接下来让我们讨论一下：\n\n您对未来几年的职业发展有什么规划？'
    ]
    
    const aiCount = messages.value.filter(m => m.role === 'ai').length
    const responseIndex = Math.min(aiCount, fallbackResponses.length - 1)
    
    messages.value.push({
      id: `ai-${Date.now()}`,
      role: 'ai',
      content: fallbackResponses[responseIndex]
    })
  } finally {
    isGenerating.value = false
    scrollToBottom()
  }
}

async function generateStudyNotes() {
  if (!sessionId.value) {
    alert('请先进行面试再生成学习笔记')
    return
  }
  
  isGeneratingStudyNotes.value = true
  
  try {
    const response = await api.post('/api/interview/study-notes', {
      session_id: sessionId.value
    })
    
    studyNotes.value = response.content
  } catch (error) {
    studyNotes.value = '生成学习笔记失败，请稍后重试。'
  } finally {
    isGeneratingStudyNotes.value = false
  }
}

function saveToNotes() {
  if (!studyNotes.value) return
  
  const newNote = {
    id: `note-${Date.now()}`,
    title: '面试学习笔记',
    content: studyNotes.value,
    created_at: new Date().toISOString()
  }
  
  appStore.notes.push(newNote)
  
  // 切换到笔记页面
  router.push('/notes')
}

function resetToInterview() {
  studyNotes.value = null
  isGeneratingStudyNotes.value = false
}

function clearMessages() {
  messages.value = []
  studyNotes.value = null
  sessionId.value = null
  isGeneratingStudyNotes.value = false
  jdContent.value = ''
}

function toggleCollection(message: any) {
  message.collected = !message.collected
  
  if (message.collected) {
    const lastUserAnswer = [...messages.value].reverse().find(m => m.role === 'user')
    if (lastUserAnswer) {
      appStore.addFavorite({
        id: message.id,
        question: message.content,
        answer: lastUserAnswer.content,
        createdAt: Date.now()
      })
    }
  } else {
    appStore.removeFavorite(message.id)
  }
}

onMounted(() => {})
</script>

<style scoped>
.interview-page {
  min-height: 100vh;
}
</style>
