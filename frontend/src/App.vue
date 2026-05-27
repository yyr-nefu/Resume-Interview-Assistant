<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-brand">
          <div class="brand-icon">
            <Cpu />
          </div>
          <span class="brand-text">AI求职助手</span>
        </div>
        <div class="nav-links">
          <router-link to="/" class="nav-link">
            <House />
            <span>首页</span>
          </router-link>
          <router-link to="/interview" class="nav-link">
            <ChatDotRound />
            <span>模拟面试</span>
          </router-link>
          <router-link to="/notes" class="nav-link">
            <Memo />
            <span>学习笔记</span>
          </router-link>
        </div>
      </div>
    </nav>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { Cpu, House, ChatDotRound, Memo } from '@element-plus/icons-vue'
</script>

<style>
:root {
  /* 主色调 */
  --primary-color: #007aff;
  --primary-light: rgba(0, 122, 255, 0.1);
  --primary-hover: #0066e6;
  --secondary-color: #5856d6;
  --accent-color: #8b5cf6;
  
  /* 背景色 */
  --bg-color: #fafafa;
  --bg-surface: #ffffff;
  --bg-gradient-start: #667eea;
  --bg-gradient-end: #764ba2;
  
  /* 文字颜色 */
  --text-primary: #1d1d1f;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --text-white: #ffffff;
  
  /* 状态颜色 */
  --success-color: #22c55e;
  --warning-color: #f59e0b;
  --error-color: #ef4444;
  --info-color: #007aff;
  
  /* 边框颜色 */
  --border-color: #e5e7eb;
  --border-light: #f3f4f6;
  
  /* 阴影 */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.12);
  --shadow-xl: 0 12px 40px rgba(0, 0, 0, 0.15);
  
  /* 圆角 */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 20px;
  --radius-2xl: 24px;
  --radius-full: 9999px;
  
  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;
  
  /* 字体大小 */
  --text-xs: 12px;
  --text-sm: 13px;
  --text-base: 14px;
  --text-lg: 15px;
  --text-xl: 16px;
  --text-2xl: 20px;
  --text-3xl: 24px;
  --text-4xl: 28px;
  
  /* 过渡 */
  --transition-fast: 0.15s ease;
  --transition-normal: 0.25s ease;
  --transition-slow: 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'Noto Sans SC', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-primary);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 var(--spacing-xl);
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.brand-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  border-radius: var(--radius-md);
}

.brand-icon .el-icon {
  font-size: 20px;
  color: var(--text-white);
}

.brand-text {
  font-size: 19px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.3px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  flex-direction: row;
}

.nav-link {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-md);
  text-decoration: none;
  color: var(--text-secondary);
  font-size: var(--text-base);
  font-weight: 500;
  transition: all var(--transition-slow);
  white-space: nowrap;
}

.nav-link:hover {
  background: var(--border-light);
  color: var(--text-primary);
  transform: translateY(-1px);
}

.nav-link.router-link-active {
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.1) 0%, rgba(88, 86, 214, 0.1) 100%);
  color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(0, 122, 255, 0.15);
}

.nav-link .el-icon {
  font-size: 17px;
}

.nav-link span {
  display: inline-block;
  vertical-align: middle;
}

.main-content {
  flex: 1;
  padding: var(--spacing-lg) var(--spacing-xl);
}

@media (max-width: 768px) {
  .nav-container {
    padding: 0 var(--spacing-md);
    height: 56px;
  }
  
  .brand-text {
    font-size: var(--text-xl);
  }
  
  .nav-link {
    padding: var(--spacing-xs) calc(var(--spacing-md) - 2px);
    font-size: var(--text-sm);
    gap: var(--spacing-xs);
  }
  
  .main-content {
    padding: var(--spacing-md);
  }
}

@media (max-width: 480px) {
  .nav-link span {
    display: none;
  }
  
  .nav-link {
    gap: 0;
    width: 40px;
    justify-content: center;
  }
  
  .brand-text {
    font-size: var(--text-lg);
  }
}
</style>
