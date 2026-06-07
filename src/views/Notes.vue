<template>
  <div class="notes-page min-h-screen">
    <div class="max-w-6xl mx-auto px-6 py-8">
      <!-- Header -->
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-white mb-3">学习笔记</h1>
        <p class="text-slate-400 max-w-2xl mx-auto">
          基于您的职位描述生成个性化学习材料，或者整理您喜爱的面试回答。
        </p>
      </div>

      <!-- Tabs -->
      <div class="flex items-center justify-center gap-2 mb-10">
        <button 
          @click="activeTab = 'notes'"
          :class="[
            'px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-200',
            activeTab === 'notes' 
              ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/30' 
              : 'text-slate-400 hover:text-white hover:bg-white/5'
          ]"
        >
          <span class="flex items-center gap-2">
            <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            学习笔记
          </span>
        </button>
        <button 
          @click="activeTab = 'favorites'"
          :class="[
            'px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-200',
            activeTab === 'favorites' 
              ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/30' 
              : 'text-slate-400 hover:text-white hover:bg-white/5'
          ]"
        >
          <span class="flex items-center gap-2">
            <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
            收藏回答
          </span>
        </button>
      </div>

      <!-- Study Notes Tab -->
      <div v-if="activeTab === 'notes'" class="max-w-3xl mx-auto">
        <div v-if="!generatedNote" class="text-center py-16 space-y-8">
          <div class="w-24 h-24 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-3xl flex items-center justify-center mx-auto">
            <svg class="w-12 h-12 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <div class="space-y-3">
            <h2 class="text-2xl font-bold text-white">生成学习笔记</h2>
            <p class="text-slate-400 max-w-md mx-auto">
              基于您提供的职位描述创建个性化学习材料。
            </p>
          </div>
          <button 
            @click="generateNotes"
            :disabled="isGenerating"
            class="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl text-white font-semibold shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center gap-2 mx-auto"
          >
            <svg v-if="isGenerating" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ isGenerating ? '生成中...' : '生成学习笔记' }}</span>
          </button>
        </div>

        <!-- Display Generated Note -->
        <div v-else class="bg-gradient-to-br from-white/5 to-white/0 border border-white/10 rounded-3xl p-8 shadow-2xl shadow-blue-500/10">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-xl font-bold text-white">您的学习指南</h3>
            <div class="flex items-center gap-2">
              <button 
                @click="copyNote"
                class="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-all duration-200 flex items-center gap-1.5 text-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                </svg>
                <span>{{ copied ? '已复制！' : '复制' }}</span>
              </button>
              <button 
                @click="saveToArchive"
                class="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-medium hover:shadow-lg hover:shadow-blue-500/30 transition-all duration-200 flex items-center gap-1.5 text-sm"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2v-2" />
                </svg>
                <span>存档</span>
              </button>
            </div>
          </div>
          <div class="prose prose-invert max-w-none">
            <div class="whitespace-pre-wrap text-slate-300 leading-relaxed">
              {{ generatedNote }}
            </div>
          </div>
        </div>
      </div>

      <!-- Favorites Tab -->
      <div v-else class="max-w-4xl mx-auto">
        <!-- Folder Management -->
        <div class="mb-8">
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg font-semibold text-white">收藏集</h3>
            <button 
              @click="createFolder"
              class="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-all duration-200 flex items-center gap-1.5 text-sm"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              <span>新建文件夹</span>
            </button>
            <button
              @click="toggleSelectionMode"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-1.5 text-sm',
                selectionMode
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg shadow-blue-500/30'
                  : 'bg-white/5 border border-white/10 text-slate-400 hover:text-white hover:bg-white/10'
              ]"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="!selectionMode" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
              <span>{{ selectionMode ? '取消选择' : '多选生成笔记' }}</span>
            </button>
          </div>

          <!-- 选择模式下的操作栏 -->
          <div v-if="selectionMode && selectedItems.size > 0" class="mb-6 p-4 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 rounded-xl flex items-center justify-between">
            <span class="text-white font-medium">已选择 {{ selectedItems.size }} 个回答</span>
            <button
              @click="generateNoteFromFavorites"
              :disabled="isGenerating || selectedItems.size === 0"
              class="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg text-white font-semibold shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <svg v-if="isGenerating" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ isGenerating ? '生成中...' : '生成学习笔记' }}</span>
            </button>
          </div>
          
          <!-- Folders Grid -->
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-8">
            <div 
              v-for="folder in folders"
              :key="folder.id"
              @click="selectedFolderId = folder.id"
              :class="[
                'rounded-xl p-4 border-2 transition-all duration-200 cursor-pointer hover:-translate-y-1',
                selectedFolderId === folder.id 
                  ? 'border-blue-500/50 bg-gradient-to-br from-blue-500/10 to-purple-500/10 shadow-lg shadow-blue-500/20' 
                  : 'border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/10'
              ]"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="w-10 h-10 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                  </svg>
                </div>
                <span class="text-xs text-slate-400 font-medium">
                  {{ getFolderItemCount(folder.id) }}
                </span>
              </div>
              <h4 class="text-white font-semibold truncate">{{ folder.name }}</h4>
              <p class="text-slate-400 text-xs mt-1">{{ getFolderItemCount(folder.id) }} 项</p>
            </div>
          </div>

          <!-- Selected Folder Items -->
          <div v-if="selectedFolderId" class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-lg font-semibold text-white">
                {{ getSelectedFolderName() }}
              </h3>
              <button 
                @click="selectedFolderId = null"
                class="text-slate-400 hover:text-white text-sm transition-colors"
              >
                返回全部文件夹
              </button>
            </div>
            
            <div class="space-y-3">
              <div
                v-for="item in getFolderItems()"
                :key="item.id"
                :class="[
                  'rounded-xl transition-all duration-200',
                  selectionMode && isItemSelected(item.id)
                    ? 'bg-blue-500/10 border-2 border-blue-500/50'
                    : 'bg-white/5 border border-white/10 hover:border-blue-500/30 hover:bg-white/10'
                ]"
              >
                <div
                  @click="selectionMode ? toggleSelection(item.id) : (expandedItemId = expandedItemId === item.id ? null : item.id)"
                  class="p-5 cursor-pointer flex items-start justify-between gap-4"
                >
                  <!-- 选择模式下的复选框 -->
                  <div v-if="selectionMode" class="shrink-0 pt-1">
                    <div
                      :class="[
                        'w-5 h-5 rounded-md border-2 flex items-center justify-center transition-all duration-200',
                        isItemSelected(item.id)
                          ? 'bg-blue-500 border-blue-500'
                          : 'border-slate-400 bg-transparent'
                      ]"
                    >
                      <svg v-if="isItemSelected(item.id)" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                      </svg>
                    </div>
                  </div>

                  <div class="flex-1 min-w-0">
                    <div class="mb-3">
                      <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-blue-500/10 text-blue-300 text-xs font-semibold rounded-full">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        问题
                      </span>
                    </div>
                    <p class="text-white font-medium mb-3" :class="{ 'line-clamp-2': expandedItemId !== item.id }">{{ item.question }}</p>
                    <div class="mb-3">
                      <span class="inline-flex items-center gap-1.5 px-2.5 py-1 bg-emerald-500/10 text-emerald-300 text-xs font-semibold rounded-full">
                        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                        </svg>
                        回答
                      </span>
                    </div>
                    <p class="text-slate-400 text-sm whitespace-pre-wrap leading-relaxed" :class="{ 'line-clamp-3': expandedItemId !== item.id }">{{ item.answer }}</p>
                    <p class="text-slate-500 text-xs mt-3">
                      {{ formatDate(item.createdAt) }}
                    </p>
                  </div>

                  <div class="flex flex-col gap-2 shrink-0">
                    <button
                      @click.stop
                      class="p-2 text-slate-400 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200"
                      title="{{ expandedItemId === item.id ? '收起' : '展开' }}"
                    >
                      <svg v-if="expandedItemId !== item.id" class="w-4.5 h-4.5 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                      </svg>
                      <svg v-else class="w-4.5 h-4.5 transition-transform duration-200 rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                      </svg>
                    </button>
                    <button 
                      @click.stop="moveItem(item)"
                      class="p-2 text-slate-400 hover:text-white hover:bg-white/10 rounded-lg transition-all duration-200"
                      title="移动到其他文件夹"
                    >
                      <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
                      </svg>
                    </button>
                    <button 
                      @click.stop="removeItem(item.id)"
                      class="p-2 text-slate-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-all duration-200"
                      title="删除"
                    >
                      <svg class="w-4.5 h-4.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>

                <!-- 展开后的操作栏 -->
                <div v-if="expandedItemId === item.id" class="px-5 pb-5 pt-0 border-t border-white/5">
                  <div class="flex items-center gap-3 mt-4 pt-4">
                    <button
                      @click.stop="copyAnswer(item.answer)"
                      class="px-4 py-2 bg-white/5 border border-white/10 rounded-lg text-slate-400 hover:text-white hover:bg-white/10 transition-all duration-200 flex items-center gap-1.5 text-sm"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                      </svg>
                      <span>复制回答</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <div v-if="getFolderItems().length === 0" class="text-center py-10">
              <p class="text-slate-400">该文件夹中暂无收藏的回答。</p>
            </div>
          </div>

          <div v-else class="text-center py-10">
            <p class="text-slate-400">请选择一个文件夹查看您收藏的回答。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAppStore } from '@/stores/app'
import api from '@/utils/api'

const appStore = useAppStore()

const activeTab = ref<'notes' | 'favorites'>('notes')
const isGenerating = ref(false)
const generatedNote = ref<string | null>(null)
const copied = ref(false)
const selectedFolderId = ref<string | null>(null)
const expandedItemId = ref<string | null>(null)

// 多选模式
const selectionMode = ref(false)
const selectedItems = ref<Set<string>>(new Set())
const folders = ref([
  { id: 'all', name: '全部回答' },
  { id: 'behavioral', name: '行为面试' },
  { id: 'technical', name: '技术面试' },
  { id: 'product', name: '产品相关' }
])

// Mock study content
const mockStudyNote = `# 学习指南 - 前端开发工程师

## 需要重点关注的技能

1. **Vue3 & 现代框架**
   - 组件模式和组合式 API
   - 状态管理 (Pinia, Vuex)
   - 服务端渲染 (Nuxt.js)

2. **TypeScript 精通**
   - 高级类型
   - 泛型组件
   - 类型安全模式

3. **性能优化**
   - 代码分割
   - 懒加载
   - Vue 的性能优化技巧

## 常见面试问题

1. 您如何优化 Vue 应用程序的性能？
2. 请解释 Vue3 组合式 API 及其使用场景
3. 您会如何结构一个大型 Vue 应用程序？

## 行动清单

- 回顾您简历中的项目并准备 STAR 故事
- 练习重点关注 Vue 模式的编程挑战
- 学习前端应用的系统设计`

function generateNotes() {
  isGenerating.value = true
  
  setTimeout(() => {
    generatedNote.value = mockStudyNote
    isGenerating.value = false
  }, 2000)
}

function copyNote() {
  if (!generatedNote.value) return
  
  navigator.clipboard.writeText(generatedNote.value)
  copied.value = true
  setTimeout(() => {
    copied.value = false
  }, 2000)
}

function saveToArchive() {
  alert('已保存到存档！')
}

function createFolder() {
  const name = prompt('请输入文件夹名称：')
  if (name) {
    folders.value.push({
      id: name.toLowerCase().replace(/\s+/g, '-'),
      name: name
    })
  }
}

function getFolderItemCount(folderId: string): number {
  if (folderId === 'all') {
    return appStore.favorites.length
  }
  return appStore.favorites.filter(f => f.folderId === folderId).length
}

function getFolderItems() {
  if (!selectedFolderId.value) return []
  
  if (selectedFolderId.value === 'all') {
    return appStore.favorites
  }
  return appStore.favorites.filter(f => f.folderId === selectedFolderId.value)
}

function getSelectedFolderName() {
  if (!selectedFolderId.value) return ''
  return folders.value.find(f => f.id === selectedFolderId.value)?.name || ''
}

function formatDate(timestamp: number) {
  return new Date(timestamp).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function moveItem(item: any) {
  alert('移动功能 - 将打开文件夹选择器')
}

function removeItem(id: string) {
  if (confirm('确定要删除这个收藏的回答吗？')) {
    appStore.removeFavorite(id)
  }
}

function copyAnswer(text: string) {
  navigator.clipboard.writeText(text)
}

// 多选功能
function toggleSelection(itemId: string) {
  if (selectedItems.value.has(itemId)) {
    selectedItems.value.delete(itemId)
  } else {
    selectedItems.value.add(itemId)
  }
  // 触发响应式更新
  selectedItems.value = new Set(selectedItems.value)
}

function toggleSelectionMode() {
  selectionMode.value = !selectionMode.value
  if (!selectionMode.value) {
    selectedItems.value.clear()
    expandedItemId.value = null
  }
}

function isItemSelected(itemId: string): boolean {
  return selectedItems.value.has(itemId)
}

// 从收藏生成笔记
async function generateNoteFromFavorites() {
  if (selectedItems.value.size === 0) {
    alert('请至少选择一个收藏的回答')
    return
  }

  isGenerating.value = true

  try {
    // 获取选中的项目
    const items = getFolderItems().filter(item => selectedItems.value.has(item.id))

    const response = await api.post('/api/note/generate-from-favorites', {
      items: items.map(item => ({
        question: item.question,
        answer: item.answer
      }))
    })

    generatedNote.value = response.content || '生成失败，请重试'
    activeTab.value = 'notes'  // 切换到笔记tab显示结果
    selectionMode.value = false
    selectedItems.value.clear()

  } catch (error) {
    console.error('生成笔记失败:', error)
    alert('生成笔记失败，请稍后重试')
  } finally {
    isGenerating.value = false
  }
}
</script>

<style scoped>
.notes-page {
  min-height: 100vh;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
