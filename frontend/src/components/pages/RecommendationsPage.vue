<template>
  <div class="page-content">
    <div class="page-header">
      <h1 class="page-title">Book Recommendations</h1>
      <p class="page-subtitle">Based on your subscriptions</p>
    </div>

    <div class="recommendations-grid">
      <div class="recommendation-card" v-for="book in books" :key="book.title">
        <div class="book-cover-container">
          <img class="book-cover" :src="book.cover" :alt="book.title" />
        </div>
        <div class="book-details">
          <h3 class="book-title">{{ book.title }}</h3>
          <span class="book-author">{{ book.author }}</span>
          <p class="book-info">{{ book.description }}</p>
          <button class="reviews-button">See Reviews</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const books = ref([
  {
    title: 'The Silent Patient',
    author: 'Alex Michaelides',
    cover: 'https://m.media-amazon.com/images/I/81bsw6fnUiL._AC_UF1000,1000_QL80_.jpg',
    description: 'A psychological thriller about a woman who shoots her husband and then stops speaking.'
  },
  {
    title: 'Educated',
    author: 'Tara Westover',
    cover: 'https://m.media-amazon.com/images/I/71m+Qtq+HUL._AC_UF1000,1000_QL80_.jpg',
    description: 'A memoir about a woman who leaves her survivalist family and goes on to earn a PhD.'
  },
  {
    title: 'Sapiens',
    author: 'Yuval Noah Harari',
    cover: 'https://m.media-amazon.com/images/I/713jIoMO3UL._AC_UF1000,1000_QL80_.jpg',
    description: 'A brief history of humankind, exploring the evolution of our species.'
  },
  {
    title: 'The Midnight Library',
    author: 'Matt Haig',
    cover: 'https://m.media-amazon.com/images/I/81WZ6QvGZ2L._AC_UF1000,1000_QL80_.jpg',
    description: 'A novel about a library between life and death where each book represents a different life path.'
  }
])
</script>
