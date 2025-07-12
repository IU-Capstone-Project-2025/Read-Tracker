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
    
    <div v-if="isAuthenticated" class="toggle-btn" @click="goBack">
      <
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavigationPanel from './components/NavigationPanel.vue'
import { useAuthStore } from '@/store/auth'
import { useBooksStore } from '@/store/books'

const router = useRouter()
const isCollapsed = ref(false)
const authStore = useAuthStore()
const booksStore = useBooksStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(async () => {
  if (authStore.token) {
    await authStore.fetchProfile()
  }
  if (!booksStore.books.length && isAuthenticated.value) {
    await booksStore.fetchBooks()
  }
})

const currentPage = computed(() => {
  return router.currentRoute.value.name || 'recommendations'
})

const goBack = () => {
  router.back()
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