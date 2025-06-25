<template>
  <div class="page-content">
    <div class="page-header">
      <h1 class="page-title">My Books</h1>
      <p class="page-subtitle">Your personal reading collection</p>
    </div>

    <div class="books-header">
      <h3>Filter by Status:</h3>
      <div class="filter-container">
        <button
          class="filter-button"
          :class="{ active: currentFilter === 'all' }"
          @click="currentFilter = 'all'"
        >
          All Books
        </button>
        <button
          class="filter-button"
          :class="{ active: currentFilter === 'to read' }"
          @click="currentFilter = 'to read'"
        >
          To Read
        </button>
        <button
          class="filter-button"
          :class="{ active: currentFilter === 'reading' }"
          @click="currentFilter = 'reading'"
        >
          Reading
        </button>
        <button
          class="filter-button"
          :class="{ active: currentFilter === 'read' }"
          @click="currentFilter = 'read'"
        >
          Have Read
        </button>
      </div>
    </div>

    <div class="books-grid">
      <div class="book-card" v-for="book in filteredBooks" :key="book.id">
        <div class="book-card-cover" :style="{ backgroundImage: `url(${book.cover})` }"></div>
        <div class="book-card-details">
          <div class="book-status" :class="'status-' + book.status.replace(' ', '-')">
            {{ statusLabels[book.status] }}
          </div>
          <h3 class="book-title">{{ book.title }}</h3>
          <span class="book-author">{{ book.author }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const currentFilter = ref('all')

const books = ref([
  {
    id: 1,
    title: 'Project Hail Mary',
    author: 'Andy Weir',
    cover: 'https://m.media-amazon.com/images/I/91Bc+UJQn0L._AC_UF1000,1000_QL80_.jpg',
    status: 'read'
  },
  {
    id: 2,
    title: 'The Midnight Library',
    author: 'Matt Haig',
    cover: 'https://m.media-amazon.com/images/I/81WZ6QvGZ2L._AC_UF1000,1000_QL80_.jpg',
    status: 'reading'
  },
  {
    id: 3,
    title: 'The Silent Patient',
    author: 'Alex Michaelides',
    cover: 'https://m.media-amazon.com/images/I/81bsw6fnUiL._AC_UF1000,1000_QL80_.jpg',
    status: 'read'
  },
  {
    id: 4,
    title: 'Educated',
    author: 'Tara Westover',
    cover: 'https://m.media-amazon.com/images/I/71m+Qtq+HUL._AC_UF1000,1000_QL80_.jpg',
    status: 'reading'
  },
  {
    id: 5,
    title: 'Atomic Habits',
    author: 'James Clear',
    cover: 'https://m.media-amazon.com/images/I/91uwocAMtSL._AC_UF1000,1000_QL80_.jpg',
    status: 'to read'
  },
  {
    id: 6,
    title: 'Sapiens',
    author: 'Yuval Noah Harari',
    cover: 'https://m.media-amazon.com/images/I/713jIoMO3UL._AC_UF1000,1000_QL80_.jpg',
    status: 'read'
  }
])

const statusLabels = {
  'to read': 'To Read',
  'reading': 'Reading',
  'read': 'Have Read'
}

const filteredBooks = computed(() => {
  if (currentFilter.value === 'all') return books.value
  return books.value.filter(book => book.status === currentFilter.value)
})
</script>
