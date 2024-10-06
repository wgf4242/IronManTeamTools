import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {path: '/', name: 'home', component: HomeView},
    { path: '/', redirect: '/common' },
    {path: '/common', name: 'common', component: () => import('@/views/Temp.vue')},
    {path: '/aes', name: 'aes', component: () => import('@/views/Crypto_AES.vue')},
    {path: '/coordinate', name: 'coordinate', component: () => import('@/views/Coordinate.vue')},
    {path: '/lsb', name: 'lsb', component: () => import('@/views/ciphers/Crypto_LSB.vue')},
    {path: '/frequency', name: 'frequency', component: () => import('@/views/ciphers/Frequency.vue')},
    {path: '/binary', name: 'binary', component: () => import('@/views/ciphers/CryptoBinary.vue')},
    {path: '/reverse_file', name: 'reverse_file', component: () => import('@/views/ciphers/ReverseFile.vue')},
    {path: '/url_component', name: 'url_component', component: () => import('@/views/web/URLComponent.vue')},

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
