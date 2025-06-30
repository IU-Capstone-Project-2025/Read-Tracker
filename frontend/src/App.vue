<template>
  <div class="app-container">
    <NavigationPanel
      :is-collapsed="isCollapsed"
      :current-page="currentPage"
      @toggle-sidebar="toggleSidebar"
      @navigate="changePage"
    />
    <div class="main-content">
      <router-view />
    </div>
    <div class="toggle-btn" @click="toggleSidebar">
      {{ isCollapsed ? '>' : '<' }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavigationPanel from './components/NavigationPanel.vue'
import { useAuthStore } from '@/store/auth'
import { useBooksStore } from '@/store/books'
import { fetchBooks } from '@/api/books'

const router = useRouter()
const isCollapsed = ref(false)
const authStore = useAuthStore()
const booksStore = useBooksStore()

onMounted(() => {
  // Initialize user if token exists
  if (authStore.token) {
    authStore.fetchProfile().catch(() => {
      // Handle token expiration or invalid token
      authStore.logout()
    })
  }
  
  // Load books if not already loaded
  if (!booksStore.books.length) {
    loadBooks()
  }
})

async function loadBooks() {
  try {
    const booksData = await fetchBooks()
    booksStore.initializeBooks(booksData)
  } catch (error) {
    console.error('Failed to load books:', error)
  }
}

const currentPage = computed(() => {
  return router.currentRoute.value.name || 'recommendations'
})

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const changePage = (page) => {
  router.push({ name: page })
}
</script>