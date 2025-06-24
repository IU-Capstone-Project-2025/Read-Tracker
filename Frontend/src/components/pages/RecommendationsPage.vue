<template>
  <div class="page-content">
    <div class="page-header">
      <h1 class="page-title">Book Recommendations</h1>
      <p class="page-subtitle">Based on your subscriptions</p>
    </div>

    <div class="recommendations-grid">
      <div 
        class="recommendation-card" 
        v-for="book in books" 
        :key="book.id"
        @click="goToBookProfile(book.id)"
      >
        <div class="book-cover-container">
          <img class="book-cover" :src="book.cover" :alt="book.title" />
        </div>
        <div class="book-details">
          <h3 class="book-title">{{ book.title }}</h3>
          <span class="book-author">{{ book.author }}</span>
          <p class="book-info">{{ book.description }}</p>
          <button class="reviews-button">See Details</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import booksData from '@/data/books'

const router = useRouter()
const books = ref(booksData)

const goToBookProfile = (bookId) => {
  router.push({ name: 'bookProfile', params: { id: bookId } })
}
</script>

<style scoped>
.recommendation-card {
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.recommendation-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}
</style>