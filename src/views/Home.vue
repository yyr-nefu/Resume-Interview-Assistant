<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="relative py-20 px-6">
      <div class="max-w-7xl mx-auto">
        <div class="max-w-3xl mx-auto text-center">
          <div class="space-y-8">
            <div class="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-full border border-blue-500/20">
              <span class="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
              <span class="text-sm text-blue-300 font-medium">AI 驱动的职业提升</span>
            </div>
            
            <div class="space-y-4">
              <h1 class="text-5xl lg:text-6xl font-bold text-white leading-tight">
                提升您的
                <span class="bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
                  职业旅程
                </span>
              </h1>
              <p class="text-lg text-slate-400 leading-relaxed max-w-lg">
                通过 AI 驱动的洞察、个性化的面试辅导和精准的学习材料，彻底改变您的求职过程。更快地获得理想职位。
              </p>
            </div>
            
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                @click="scrollToForm"
                class="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl text-white font-semibold shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-[1.02] transition-all duration-300 flex items-center justify-center gap-2"
              >
                <span>免费开始使用</span>
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </button>
              <button class="px-8 py-4 bg-white/5 border border-white/10 rounded-xl text-white font-semibold hover:bg-white/10 hover:border-white/20 transition-all duration-300 flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span>观看演示</span>
              </button>
            </div>
            
            <!-- Stats -->
            <div class="grid grid-cols-3 gap-6 pt-4 max-w-md mx-auto">
              <div class="text-center">
                <div class="text-3xl font-bold text-white">10K+</div>
                <div class="text-sm text-slate-500">用户</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-white">95%</div>
                <div class="text-sm text-slate-500">成功率</div>
              </div>
              <div class="text-center">
                <div class="text-3xl font-bold text-white">24/7</div>
                <div class="text-sm text-slate-500">支持</div>
              </div>
            </div>
          </div>
          

        </div>
      </div>
    </section>
    
    <!-- Form Section -->
    <section ref="formSection" class="py-20 px-6">
      <div class="max-w-4xl mx-auto">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-white mb-4">开启您的职业蜕变</h2>
          <p class="text-slate-400 max-w-xl mx-auto">
            分享您的目标职位描述和简历，获取个性化洞察和指导。
          </p>
        </div>
        
        <div class="bg-gradient-to-br from-white/5 to-white/0 border border-white/10 rounded-3xl p-8 backdrop-blur-xl shadow-2xl shadow-blue-500/10">
          <form @submit.prevent="handleSubmit" class="space-y-6">
            <!-- JD Input -->
            <div class="space-y-3">
              <label class="flex items-center gap-2 text-white font-medium">
                <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                职位描述
              </label>
              <textarea 
                v-model="jdContent" 
                placeholder="在此粘贴完整的职位描述..."
                class="w-full h-40 bg-slate-900/50 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-all resize-none"
              />
            </div>
            
            <!-- Resume Upload -->
            <div class="space-y-3">
              <label class="flex items-center gap-2 text-white font-medium">
                <svg class="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                简历
              </label>
              <div 
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
                :class="[
                  'border-2 border-dashed rounded-xl p-12 text-center transition-all cursor-pointer',
                  isDragging 
                    ? 'border-blue-500 bg-blue-500/10' 
                    : 'border-white/10 bg-slate-900/30 hover:border-white/20 hover:bg-slate-900/50',
                  resumeFile ? 'border-emerald-500/50 bg-emerald-500/5' : ''
                ]"
              >
                <input 
                  ref="fileInput"
                  type="file" 
                  accept=".pdf,.doc,.docx,.txt"
                  class="hidden"
                  @change="handleFileChange"
                >
                
                <div v-if="!resumeFile" class="space-y-4">
                  <div class="w-16 h-16 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl flex items-center justify-center mx-auto">
                    <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  <div class="space-y-1">
                    <p class="text-white font-medium">将您的简历拖放到此处</p>
                    <p class="text-slate-500 text-sm">或点击浏览 (PDF, DOC, DOCX, TXT)</p>
                  </div>
                </div>
                
                <div v-else class="space-y-4">
                  <div class="w-16 h-16 bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 rounded-2xl flex items-center justify-center mx-auto">
                    <svg class="w-8 h-8 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <div class="space-y-1">
                    <p class="text-white font-medium">{{ resumeFile.name }}</p>
                    <p class="text-slate-500 text-sm">{{ formatFileSize(resumeFile.size) }}</p>
                  </div>
                  <button 
                    type="button"
                    @click.stop="clearResume"
                    class="px-4 py-2 text-slate-400 hover:text-white text-sm transition-colors"
                  >
                    更换文件
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Submit Button -->
            <button 
              type="submit"
              :disabled="isSubmitting || !jdContent || !resumeFile"
              class="w-full py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl text-white font-semibold shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-[1.01] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
            >
              <svg v-if="isSubmitting" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ isSubmitting ? '分析中...' : '分析并获取建议' }}</span>
            </button>
          </form>
        </div>
      </div>
    </section>
    
    <!-- Features Section -->
    <section class="py-20 px-6">
      <div class="max-w-7xl mx-auto">
        <div class="text-center mb-16">
          <h2 class="text-3xl font-bold text-white mb-4">助您成功的强大功能</h2>
          <p class="text-slate-400 max-w-xl mx-auto">
            求职过程中所需的一切，尽在一处。
          </p>
        </div>
        
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="(feature, index) in features" :key="index" 
               class="group bg-gradient-to-br from-white/5 to-white/0 border border-white/10 rounded-2xl p-6 hover:bg-white/5 hover:border-white/20 hover:-translate-y-2 transition-all duration-300">
            <div class="w-14 h-14 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl flex items-center justify-center mb-5 group-hover:scale-110 transition-transform duration-300">
              <component :is="feature.icon" class="w-7 h-7 text-blue-400" />
            </div>
            <h3 class="text-white font-semibold text-lg mb-2">{{ feature.title }}</h3>
            <p class="text-slate-400 text-sm leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAppStore } from '@/stores/app'
import {
  FileText,
  Brain,
  MessageSquare,
  BookOpen
} from 'lucide-vue-next'

const router = useRouter()
const appStore = useAppStore()

const formSection = ref<HTMLElement | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const isDragging = ref(false)
const isSubmitting = ref(false)
const jdContent = ref('')
const resumeFile = ref<File | null>(null)

const features = ref([
  {
    icon: FileText,
    title: '职位分析',
    description: '深入分析职位要求，识别关键技能和能力。'
  },
  {
    icon: Brain,
    title: '简历匹配',
    description: '智能对比您的简历与职位要求。'
  },
  {
    icon: MessageSquare,
    title: '模拟面试',
    description: 'AI 驱动的面试模拟，提供实时反馈和辅导。'
  },
  {
    icon: BookOpen,
    title: '学习笔记',
    description: '个性化学习材料和练习题。'
  }
])

function scrollToForm() {
  formSection.value?.scrollIntoView({ behavior: 'smooth' })
}

function handleDrop(event: DragEvent) {
  isDragging.value = false
  const files = event.dataTransfer?.files
  if (files && files[0]) {
    resumeFile.value = files[0]
  }
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const files = target.files
  if (files && files[0]) {
    resumeFile.value = files[0]
  }
}

function clearResume() {
  resumeFile.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

function formatFileSize(bytes: number) {
  if (bytes === 0) return '0 字节'
  const k = 1024
  const sizes = ['字节', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

async function handleSubmit() {
  if (!jdContent.value || !resumeFile.value) return
  
  isSubmitting.value = true
  
  try {
    appStore.setJdContent(jdContent.value)
    
    const reader = new FileReader()
    reader.onload = (e) => {
      const content = e.target?.result as string
      appStore.setResumeContent(content)
      router.push('/interview')
    }
    reader.readAsText(resumeFile.value)
  } catch (error) {
    console.error('Error:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}
</style>
