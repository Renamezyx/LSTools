import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/index.vue'
import TrendsStats from '../views/Trends_stats.vue'
import PushStream from '../views/push_stream.vue'
import ScriptManager from '../views/script_manager.vue'

const routes = [
  {
    path: '/',
    name: '/',
    component: Index
  },
  {
    path: '/index',
    name: 'Index',
    component: Index
  },
  {
    path: '/trends_stats',
    name: 'TrendsStats',
    component: TrendsStats
  },
  {
    path: '/push_stream',
    name: 'PushStream',
    component: PushStream
  },
  {
    path: '/script_manager',
    name: 'ScriptManager',
    component: ScriptManager
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
