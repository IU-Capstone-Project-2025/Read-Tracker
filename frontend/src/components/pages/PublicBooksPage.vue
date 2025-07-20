<template>
  <div class="public-books-page">
    <div class="page-header">
      <h1 class="page-title">All Books</h1>
      <p class="page-subtitle">Browse all available books</p>
    </div>

    <div class="books-controls">
      <div class="sort-control">
        <label>Sort by:</label>
        <select v-model="sortBy" class="filter-select">
          <option value="title">Title</option>
          <option value="author">Author</option>
        </select>
      </div>
    </div>

    <div class="books-grid">
      <div
        v-for="book in sortedBooks"
        :key="book.id"
        class="book-card"
        @click="goToBookProfile(book.id)"
      >
        <div class="book-cover-container">
          <img
            v-if="book.cover"
            :src="`/images/${book.cover}.jpg`"
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
          <p class="book-info" v-if="book.description">{{ book.description.substring(0, 100) }}...</p>
          <p class="book-info" v-else>No description available</p>
          <button class="reviews-button">View Details</button>
          <button
            v-if="!isBookInUserCollection(book.id)"
            @click.stop="addToMyBooks(book.id)"
            class="add-to-my-books-button"
          >
            Add to My Books
          </button>
          <span v-else>Already in My Books</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBooksStore } from '@/store/books'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const booksStore = useBooksStore()
const authStore = useAuthStore()
const sortBy = ref('title')

onMounted(async () => {
  if (booksStore.allBooks.length === 0) {
    await booksStore.fetchAllBooks()
  }
})

const sortedBooks = computed(() => {
  let books = [...booksStore.allBooks]
  if (sortBy.value === 'title') {
    return books.sort((a, b) => a.title.localeCompare(b.title))
  } else if (sortBy.value === 'author') {
    return books.sort((a, b) => a.author.localeCompare(b.author))
  }
  return books
})

const isBookInUserCollection = (bookId) => {
  return booksStore.userBooks.some(book => book.bookId === bookId)
}

const addToMyBooks = async (bookId) => {
  if (!authStore.isAuthenticated) {
    alert('Please log in to add books to your collection.')
    return
  }
  try {
    await booksStore.addBookToUserCollection(bookId)
  } catch (error) {
    console.error('Failed to add book to collection:', error)
  }
}

const goToBookProfile = (bookId) => {
  router.push({ name: 'bookProfile', params: { id: bookId } })
}
</script>

<style scoped>
.public-books-page {
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

.sort-control {
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

.book-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
}

.add-to-my-books-button {
  margin-top: 10px;
  padding: 8px 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-to-my-books-button:hover {
  background-color: #45a049;
}

@media (max-width: 768px) {
  .books-controls {
    flex-direction: column;
    gap: 10px;
  }
}
</style>