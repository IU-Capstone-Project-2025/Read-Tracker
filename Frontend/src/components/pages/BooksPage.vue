<template>
  <div class="books-page">
    <div class="page-header">
      <h1 class="page-title">Your Books</h1>
      <p class="page-subtitle">Manage your book collection</p>
    </div>

    <div class="books-grid">
      <div 
        v-for="book in books" 
        :key="book.id" 
        class="book-card"
        @click="goToBookProfile(book.id)"
      >
        <div class="book-cover-container">
          <img :src="book.cover" :alt="book.title" class="book-cover">
        </div>
        <div class="book-details">
          <h3 class="book-title">{{ book.title }}</h3>
          <span class="book-author">{{ book.author }}</span>
          <p class="book-info">{{ book.description.substring(0, 100) }}...</p>
          <button class="reviews-button">View Details</button>
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
.book-card {
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.book-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}
</style>