import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'
import './assets/styles.css'

import config from './runtimeConfig'

import LoginPage from './components/pages/LoginPage.vue'
import RegistrationPage from './components/pages/RegistrationPage.vue'
import ForgotPasswordPage from './components/pages/ForgotPasswordPage.vue'
import ResetPasswordPage from './components/pages/ResetPasswordPage.vue'
import RecommendationsPage from './components/pages/RecommendationsPage.vue'
import ProfilePage from './components/pages/ProfilePage.vue'
import BooksPage from './components/pages/BooksPage.vue'
import ReviewsPage from './components/pages/ReviewsPage.vue'
import CollectionsPage from './components/pages/CollectionsPage.vue'
import BookProfilePage from './components/pages/BookProfilePage.vue'
import CollectionDetailPage from './components/pages/CollectionDetailPage.vue'
import SubscriptionsPage from './components/pages/SubscriptionsPage.vue'
import { useAuthStore } from './store/auth'
import { useUsersStore } from '@/store/users'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', name: 'login', component: LoginPage, meta: { requiresGuest: true } },
    { path: '/register', name: 'register', component: RegistrationPage, meta: { requiresGuest: true } },
    { path: '/forgot-password', name: 'forgotPassword', component: ForgotPasswordPage, meta: { requiresGuest: true } },
    { path: '/reset-password', name: 'resetPassword', component: ResetPasswordPage, meta: { requiresGuest: true } },
    { path: '/', name: 'recommendations', component: RecommendationsPage, meta: { requiresAuth: true } },
    { path: '/profile', name: 'profile', component: ProfilePage, meta: { requiresAuth: true } },
    { path: '/books', name: 'books', component: BooksPage, meta: { requiresAuth: true } },
    { path: '/reviews', name: 'reviews', component: ReviewsPage, meta: { requiresAuth: true } },
    { path: '/collections', name: 'collections', component: CollectionsPage, meta: { requiresAuth: true } },
    { path: '/book/:id', name: 'bookProfile', component: BookProfilePage, props: true, meta: { requiresAuth: true } },
    { path: '/collection/:id', name: 'collectionDetail', component: CollectionDetailPage, props: true, meta: { requiresAuth: true } },
    { path: '/subscriptions', name: 'subscriptions', component: SubscriptionsPage, meta: { requiresAuth: true } },
    { path: '/:pathMatch(.*)*', redirect: '/' }
  ]
})

router.beforeEach(async (to, from, next) => {
  const userStore = useAuthStore()
  
  if (userStore.token && !userStore.isInitialized) {
    try {
      await userStore.fetchProfile()
    } catch (e) {
      console.error('Failed to init user:', e)
      userStore.logout()
      return next('/login')
    }
  }

  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    return next('/login')
  }

  if (to.meta.requiresGuest && userStore.isAuthenticated) {
    return next('/')
  }

  next()
})
const pinia = createPinia()
const app = createApp(App)

app.config.globalProperties.$config = config

app.use(router)
app.use(pinia)
app.mount('#app')
useUsersStore(pinia)

console.log('Runtime config loaded:', config)
