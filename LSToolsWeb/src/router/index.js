import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/index.vue'
import TrendsStats from '../views/Trends_stats.vue'
import PushStream from '../views/push_stream.vue'

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
