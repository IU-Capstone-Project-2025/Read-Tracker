<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">{{ collection.name }}</h1>
      <p class="page-subtitle">{{ collection.description }}</p>
      <div class="collection-meta">
        <span>{{ collection.bookCount }} books</span>
        <span>Created: {{ formatDate(collection.createdAt) }}</span>
      </div>
    </div>
    
    <div v-if="loading" class="loading">Loading books...</div>
    <div v-else class="books-grid">
      <div 
        v-for="book in books" 
        :key="book.id" 
        class="book-card"
        @click="viewBook(book.id)"
      >
        <div class="book-cover-container">
          <img 
            v-if="book.cover" 
            :src="book.cover" 
            alt="Book cover" 
            class="book-cover"
          >
          <img 
            v-else 
            src="@/public/images/placeholder.png" 
            alt="Placeholder" 
            class="book-cover"
          >
        </div>
        <div class="book-details">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">{{ book.author }}</p>
          <div class="book-actions">
            <button @click.stop="removeFromCollection(book.id)">
              <i class="fas fa-trash-alt"></i> Remove
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="books.length === 0 && !loading" class="empty-state">
      <i class="fas fa-book-open"></i>
      <p>No books in this collection yet</p>
      <button class="add-btn" @click="addBooksToCollection">
        <i class="fas fa-plus"></i> Add Books
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchCollection } from '@/api/collections'

const route = useRoute()
const router = useRouter()

const collection = ref({
  id: route.params.id,
  name: '',
  description: '',
  bookCount: 0,
  createdAt: new Date()
})
const books = ref([])
const loading = ref(true)

onMounted(async () => {
  await loadCollection()
})

async function loadCollection() {
  try {
    const data = await fetchCollection(route.params.id)
    collection.value = data.collection
    books.value = data.books
  } catch (error) {
    console.error('Error loading collection:', error)
  } finally {
    loading.value = false
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString()
}

function viewBook(bookId) {
  router.push({ name: 'bookProfile', params: { id: bookId } })
}

function removeFromCollection(bookId) {
  console.log('Remove book:', bookId)
}

function addBooksToCollection() {
  console.log('Add books to collection')
}
</script>

<style scoped>
.page-header {
  margin-bottom: 30px;
}

.collection-meta {
  display: flex;
  gap: 20px;
  margin-top: 10px;
  color: #666;
  font-size: 16px;
}

.book-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.book-card:hover {
  transform: translateY(-3px);
}

.book-actions {
  margin-top: 15px;
}

.book-actions button {
  background: #f8f9ff;
  border: 1px solid #ddd;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 14px;
}

.book-actions button:hover {
  background: #ff6b6b;
  color: white;
  border-color: #ff6b6b;
}

.empty-state {
  text-align: center;
  padding: 50px 20px;
  color: #666;
}

.empty-state i {
  font-size: 60px;
  margin-bottom: 20px;
  color: #764ba2;
}

.add-btn {
  margin-top: 20px;
  background: #764ba2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}
</style>