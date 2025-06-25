<template>
  <div class="app-container">
    <NavigationPanel
      :is-collapsed="isCollapsed"
      :current-page="currentPage"
      @toggle-sidebar="toggleSidebar"
      @navigate="changePage"
    />
    <div class="main-content">
      <component :is="currentPageComponent" />
    </div>
    <div class="toggle-btn" @click="toggleSidebar">
      {{ isCollapsed ? '>' : '<' }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import NavigationPanel from './components/NavigationPanel.vue'
import RecommendationsPage from './components/pages/RecommendationsPage.vue'
import ProfilePage from './components/pages/ProfilePage.vue'
import BooksPage from './components/pages/BooksPage.vue'
import ReviewsPage from './components/pages/ReviewsPage.vue'
import CollectionsPage from './components/pages/CollectionsPage.vue'

const isCollapsed = ref(false)
const currentPage = ref('recommendations')

const currentPageComponent = computed(() => {
  return {
    recommendations: RecommendationsPage,
    profile: ProfilePage,
    books: BooksPage,
    reviews: ReviewsPage,
    collections: CollectionsPage,
  }[currentPage.value]
})

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
}

const changePage = (page) => {
  currentPage.value = page
}
</script>
