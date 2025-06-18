<template>
  <div class="profile-container">
    <div class="page-header">
      <h1 class="page-title">My Reviews</h1>
      <p class="page-subtitle">Your thoughts on the books you've read</p>
    </div>

    <div class="recommendations-grid">
      <div class="recommendation-card" v-for="review in reviews" :key="review.title">
        <div class="book-cover-container">
          <img class="book-cover" :src="review.cover" :alt="review.title" />
        </div>
        <div class="book-details">
          <h3 class="book-title">{{ review.title }}</h3>
          <span class="book-author">{{ review.author }}</span>
          <div class="review-rating">{{ review.rating }}/10</div>
          <p class="book-info">"{{ review.text }}"</p>
          <button class="reviews-button">Edit Review</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const reviews = ref([
  {
    title: 'The Silent Patient',
    author: 'Alex Michaelides',
    cover: 'https://m.media-amazon.com/images/I/81bsw6fnUiL._AC_UF1000,1000_QL80_.jpg',
    rating: 8,
    text: 'A mind-blowing thriller with an ending I never saw coming. The character development was exceptional.'
  },
  {
    title: 'Project Hail Mary',
    author: 'Andy Weir',
    cover: 'https://m.media-amazon.com/images/I/91Bc+UJQn0L._AC_UF1000,1000_QL80_.jpg',
    rating: 9,
    text: 'Science fiction at its best! The problem-solving aspects reminded me of The Martian, but with even higher stakes.'
  },
  {
    title: 'The Midnight Library',
    author: 'Matt Haig',
    cover: 'https://m.media-amazon.com/images/I/81WZ6QvGZ2L._AC_UF1000,1000_QL80_.jpg',
    rating: 8,
    text: 'A beautiful exploration of life\'s possibilities. Made me appreciate the choices I\'ve made in my own life.'
  }
])
</script>
