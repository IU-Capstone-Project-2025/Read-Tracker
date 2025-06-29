import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from './App.vue'
import './assets/styles.css'

// Import components
import RecommendationsPage from './components/pages/RecommendationsPage.vue'
import ProfilePage from './components/pages/ProfilePage.vue'
import BooksPage from './components/pages/BooksPage.vue'
import ReviewsPage from './components/pages/ReviewsPage.vue'
import CollectionsPage from './components/pages/CollectionsPage.vue'
import BookProfilePage from './components/pages/BookProfilePage.vue'
import CollectionDetailPage from './components/pages/CollectionDetailPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'recommendations', component: RecommendationsPage },
    { path: '/profile', name: 'profile', component: ProfilePage },
    { path: '/books', name: 'books', component: BooksPage },
    { path: '/reviews', name: 'reviews', component: ReviewsPage },
    { path: '/collections', name: 'collections', component: CollectionsPage },
    { path: '/book/:id', name: 'bookProfile', component: BookProfilePage, props: true },
    { path: '/collection/:id', name: 'collectionDetail', component: CollectionDetailPage, props: true }
  ]
})

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)
app.mount('#app')