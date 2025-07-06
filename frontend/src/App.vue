<template>
  <div class="app-container">
    <NavigationPanel
      v-if="isAuthenticated"
      :is-collapsed="isCollapsed"
      :current-page="currentPage"
      @toggle-sidebar="toggleSidebar"
      @navigate="changePage"
    />
    
    <div class="main-content" :class="{ 'full-width': !isAuthenticated }">
      <router-view />
    </div>
    
    <div v-if="isAuthenticated" class="toggle-btn" @click="toggleSidebar">
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

const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(() => {
  if (authStore.token) {
    authStore.fetchProfile()
  }
  if (!booksStore.books.length && isAuthenticated.value) {
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

<style scoped>
.full-width {
  margin-left: 0;
  width: 100%;
}

.main-content {
  transition: all 0.3s ease;
}
</style>