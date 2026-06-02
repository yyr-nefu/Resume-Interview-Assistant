<template>
  <div id="app" class="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">
    <!-- Decorative Background Elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 left-0 w-[500px] h-[500px] bg-gradient-to-br from-blue-500/10 to-purple-500/5 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2" />
      <div class="absolute bottom-0 right-0 w-[600px] h-[600px] bg-gradient-to-br from-emerald-500/10 to-cyan-500/5 rounded-full blur-3xl translate-x-1/3 translate-y-1/3" />
      <div class="absolute top-1/2 left-1/2 w-[400px] h-[400px] bg-gradient-to-br from-amber-500/5 to-orange-500/5 rounded-full blur-3xl -translate-x-1/2 -translate-y-1/2" />
    </div>
    
    <div class="relative z-10">
      <!-- Navigation -->
      <nav class="fixed top-0 left-0 right-0 z-50 bg-slate-900/70 backdrop-blur-2xl border-b border-white/5">
        <div class="max-w-7xl mx-auto px-6 py-4">
          <div class="flex items-center justify-between">
            <!-- Logo -->
            <router-link to="/" class="flex items-center gap-3 group">
              <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg shadow-blue-500/25 group-hover:shadow-blue-500/40 transition-all duration-300 group-hover:scale-105">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="flex flex-col">
                <span class="text-xl font-bold bg-gradient-to-r from-white via-blue-100 to-white bg-clip-text text-transparent">
                  AI 求职助手
                </span>
                <span class="text-xs text-slate-400 -mt-0.5">职业提升平台</span>
              </div>
            </router-link>
            
            <!-- Navigation Links -->
            <div class="flex items-center gap-2">
              <router-link 
                v-for="item in navItems" 
                :key="item.path" 
                :to="item.path" 
                :class="[
                  'flex items-center gap-2 px-4 py-2.5 rounded-xl transition-all duration-300 font-medium text-sm',
                  isActive(item.path) 
                    ? 'bg-gradient-to-r from-blue-500/10 to-purple-500/10 text-blue-300 border border-blue-500/20 shadow-lg shadow-blue-500/10' 
                    : 'text-slate-400 hover:text-white hover:bg-white/5'
                ]"
              >
                <component :is="item.icon" class="w-4.5 h-4.5" />
                <span>{{ item.name }}</span>
              </router-link>
            </div>
            
            <!-- Action Button -->
            <div class="flex items-center gap-3">
              <a href="#" class="text-slate-400 hover:text-white transition-colors text-sm font-medium">
                帮助中心
              </a>
              <button class="px-5 py-2.5 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl text-white font-medium text-sm shadow-lg shadow-blue-500/25 hover:shadow-blue-500/40 hover:scale-105 transition-all duration-300">
                立即开始
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      <!-- Main Content -->
      <main class="pt-24 pb-16">
        <router-view />
      </main>
      
      <!-- Footer -->
      <footer class="border-t border-white/5 bg-slate-900/50">
        <div class="max-w-7xl mx-auto px-6 py-12">
          <div class="grid grid-cols-4 gap-8">
            <div class="col-span-1">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <span class="text-lg font-bold text-white">AI 求职助手</span>
              </div>
              <p class="text-slate-400 text-sm leading-relaxed">
                通过 AI 驱动的洞察和个性化指导，赋能您的职业发展之旅。
              </p>
            </div>
            
            <div>
              <h4 class="text-white font-semibold mb-4">产品</h4>
              <ul class="space-y-3">
                <li><a href="#" class="text-slate-400 hover:text-white transition-colors text-sm">功能特性</a></li>
                <li><a href="#" class="text-slate-400 hover:text-white transition-colors text-sm">价格方案</a></li>
                <li><a href="#" class="text-slate-400 hover:text-white transition-colors text-sm">集成方案</a></li>
              </ul>
            </div>
            
            <div>
              <h4 class="text-white font-semibold mb-4">公司</h4>
              <ul class="space-y-3">
                <li><a href="#" class="text-slate-400 hover:text-white transition-colors text-sm">关于我们</a></li>
                <li><a href="#" class="text-slate-400 hover:text-white transition-colors text-sm">博客</a></li>
                <li><a href="#" class="text-slate-400 hover:text-white transition-colors text-sm">招聘</a></li>
              </ul>
            </div>
            
            <div>
              <h4 class="text-white font-semibold mb-4">支持</h4>
              <ul class="space-y-3">
                <li><a href="#" class="text-slate-400 hover:text-white transition-colors text-sm">帮助中心</a></li>
                <li><a href="#" class="text-slate-400 hover:text-white transition-colors text-sm">联系方式</a></li>
                <li><a href="#" class="text-slate-400 hover:text-white transition-colors text-sm">隐私政策</a></li>
              </ul>
            </div>
          </div>
          
          <div class="border-t border-white/5 mt-12 pt-8 flex items-center justify-between">
            <p class="text-slate-500 text-sm">© 2024 AI 求职助手. 保留所有权利。</p>
            <div class="flex items-center gap-4">
              <a href="#" class="w-9 h-9 bg-white/5 rounded-lg flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/10 transition-all">
                <svg class="w-4.5 h-4.5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                </svg>
              </a>
              <a href="#" class="w-9 h-9 bg-white/5 rounded-lg flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/10 transition-all">
                <svg class="w-4.5 h-4.5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
              </a>
              <a href="#" class="w-9 h-9 bg-white/5 rounded-lg flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/10 transition-all">
                <svg class="w-4.5 h-4.5" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore } from '@/stores/app'
import {
  Home,
  MessageSquare,
  BookOpen,
  User
} from 'lucide-vue-next'

const route = useRoute()
const appStore = useAppStore()

const navItems = ref([
  { name: '首页', path: '/', icon: Home },
  { name: '模拟面试', path: '/interview', icon: MessageSquare },
  { name: '学习笔记', path: '/notes', icon: BookOpen }
])

function isActive(path: string) {
  return route.path === path
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(148, 163, 184, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(148, 163, 184, 0.5);
}

/* Animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
  }
  50% {
    box-shadow: 0 0 40px rgba(59, 130, 246, 0.6);
  }
}

.floating {
  animation: float 6s ease-in-out infinite;
}

.pulse-glow {
  animation: pulse-glow 2s ease-in-out infinite;
}
</style>