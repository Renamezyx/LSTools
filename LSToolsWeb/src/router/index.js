import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/index.vue'
import TrendsStats from '../views/Trends_stats.vue'
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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
