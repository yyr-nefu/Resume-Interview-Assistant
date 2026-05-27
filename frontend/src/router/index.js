import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Interview from '../views/Interview.vue'
import Notes from '../views/Notes.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/interview', name: 'Interview', component: Interview },
  { path: '/notes', name: 'Notes', component: Notes }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
