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
import { useSubscriptionsStore } from '@/store/subscriptions'

const router = useRouter()
const isCollapsed = ref(false)
const authStore = useAuthStore()
const booksStore = useBooksStore()
const subscriptionsStore = useSubscriptionsStore()

const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(async () => {
  if (authStore.token) {
    await authStore.fetchProfile()
    await booksStore.fetchBooks()
    await subscriptionsStore.fetchSubscriptions(authStore.user.id)
  }
})

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
.app-container {
  display: flex;
  min-height: 100vh;
  position: relative;
}

.main-content {
  flex: 1;
  padding: 20px;
  transition: all 0.3s ease;
  margin-left: 0px;
  width: calc(100% - 250px);
}

.full-width {
  margin-left: 0;
  width: 100%;
}

.toggle-btn {
  position: fixed;
  bottom: 20px;
  left: 230px;
  background: #5d3787;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 1000;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100%;
  }
}
</style>