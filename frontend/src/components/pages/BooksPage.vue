<template>
  <div class="books-page">
    <div class="page-header">
      <h1 class="page-title">Your Books</h1>
      <p class="page-subtitle">Manage your book collection</p>
    </div>

    <div class="books-controls">
      <div class="status-filter">
        <label>Filter by status:</label>
        <select v-model="statusFilter" class="filter-select">
          <option value="all">All Books</option>
          <option value="to-read">To Read</option>
          <option value="reading">Reading</option>
          <option value="completed">Completed</option>
        </select>
      </div>
      <div class="sort-control">
        <label>Sort by:</label>
        <select v-model="sortBy" class="filter-select">
          <option value="title">Title</option>
          <option value="status">Status</option>
          <option value="added">Recently Added</option>
        </select>
      </div>
    </div>

    <div class="books-grid">
      <div 
        v-for="book in filteredBooks" 
        :key="book.id" 
        class="book-card"
        @click="goToBookProfile(book.id)"
      >
        <div class="book-cover-container">
          <img 
            v-if="book.cover" 
            :src="book.cover" 
            :alt="book.title" 
            class="book-cover"
          />
          <img 
            v-else 
            src="/images/placeholder.png" 
            alt="No cover available" 
            class="book-cover"
          />
        </div>
        <div class="book-details">
          <h3 class="book-title">{{ book.title }}</h3>
          <span class="book-author">{{ book.author }}</span>
          
          <div class="book-status">
            <label>Status:</label>
            <select 
              v-model="book.status" 
              @click.stop
              @change="updateBookStatus(book)"
              class="status-select"
            >
              <option value="to-read">To Read</option>
              <option value="reading">Reading</option>
              <option value="completed">Completed</option>
            </select>
          </div>
          
          <p class="book-info" v-if="book.description">{{ book.description.substring(0, 100) }}...</p>
          <p class="book-info" v-else>No description available</p>
          <button class="reviews-button">View Details</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBooksStore } from '@/store/books'

const router = useRouter()
const booksStore = useBooksStore()

const statusFilter = ref('all')
const sortBy = ref('title')

onMounted(async () => {
  const loadedBooks = await booksStore.fetchBooks()
  if (booksStore.books.length === 0) {
    booksStore.initializeBooks(
      loadedBooks.map(book => ({
        ...book,
        status: 'to-read',       
        addedDate: Date.now() 
      }))
    )
  }
})

const filteredBooks = computed(() => {
  let filtered = [...booksStore.books]

  if (statusFilter.value !== 'all') {
    filtered = filtered.filter(book => book.status === statusFilter.value)
  }
  switch (sortBy.value) {
    case 'title':
      return filtered.sort((a, b) => a.title.localeCompare(b.title))
    case 'status':
      const statusOrder = { 'to-read': 1, 'reading': 2, 'completed': 3 }
      return filtered.sort((a, b) => statusOrder[a.status] - statusOrder[b.status])
    case 'added':
      return filtered.sort((a, b) => b.addedDate - a.addedDate)
    default:
      return filtered
  }
})

const goToBookProfile = (bookId) => {
  router.push({ name: 'bookProfile', params: { id: bookId } })
}

const updateBookStatus = (book) => {
  booksStore.updateBookStatus(book.id, book.status)
}
</script>

<style scoped>
.books-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.books-controls {
  display: flex;
  gap: 20px;
  margin-bottom: 25px;
  padding: 15px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.status-filter, .sort-control {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
}

.book-card {
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.book-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.book-status {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-select {
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
}

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
}

@media (max-width: 768px) {
  .books-controls {
    flex-direction: column;
    gap: 10px;
  }
}
</style>
