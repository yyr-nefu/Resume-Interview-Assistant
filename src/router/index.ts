import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Home from '@/views/Home.vue'
import Interview from '@/views/Interview.vue'
import Notes from '@/views/Notes.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '首页 - JD解析与简历诊断' }
  },
  {
    path: '/interview',
    name: 'Interview',
    component: Interview,
    meta: { title: '模拟面试' }
  },
  {
    path: '/notes',
    name: 'Notes',
    component: Notes,
    meta: { title: '学习笔记' }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  }
})

router.beforeEach((to, _from, next) => {
  document.title = to.meta.title as string || 'AI简历助手'
  next()
})

export default router
