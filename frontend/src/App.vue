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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import NavigationPanel from './components/NavigationPanel.vue'

const router = useRouter()
const isCollapsed = ref(false)

const currentPage = computed(() => {
  const routeName = router.currentRoute.value.name
  return routeName || 'recommendations'
})

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const changePage = (page) => {
  router.push({ name: page })
}
</script>
