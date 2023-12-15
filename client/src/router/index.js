import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', name: 'home', component: HomeView},
    {path: '/common', name: 'common', component: () => import('@/components/Temp.vue')},
    {path: '/aes', name: 'aes', component: () => import('@/components/Crypto_AES.vue')},
    {path: '/coordinate', name: 'coordinate', component: () => import('@/components/Coordinate.vue')},
    {path: '/lsb', name: 'lsb', component: () => import('@/components/ciphers/Crypto_LSB.vue')},
    {path: '/frequency', name: 'frequency', component: () => import('@/components/ciphers/Frequency.vue')},

    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
