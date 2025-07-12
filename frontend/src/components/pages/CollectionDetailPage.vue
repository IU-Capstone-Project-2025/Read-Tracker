<template>
  <div class="page">
    <div class="page-header">
      <div class="header-top">
        <h1 class="page-title">{{ collection.title }}</h1>
        <button v-if="collection.isPrivate" class="private-badge">
          <i class="fas fa-lock"></i> Private
        </button>
      </div>
      
      <p class="page-subtitle">{{ collection.description }}</p>
      
      <div class="collection-meta">
        <div class="meta-item">
          <i class="fas fa-book"></i>
          <span>{{ collection.bookCount }} books</span>
        </div>
        <div class="meta-item">
          <i class="fas fa-calendar"></i>
          <span>Created: {{ formatDate(collection.createdAt) }}</span>
        </div>
      </div>
      
      <div class="collection-actions" v-if="books.length > 0">
        <button class="action-btn primary" @click="addBooksToCollection">
          <i class="fas fa-plus"></i> Add Books
        </button>
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      <i class="fas fa-spinner fa-spin"></i> Loading books...
    </div>
    
    <div v-else-if="books.length === 0" class="empty-state">
      <div class="empty-illustration">
        <i class="fas fa-book-open"></i>
      </div>
      <h3>No Books in This Collection</h3>
      <p>Add books to get started with your collection</p>
      <button class="primary-btn" @click="addBooksToCollection">
        <i class="fas fa-plus"></i> Add Books
      </button>
    </div>
    
    <div v-else class="books-grid">
      <div 
        v-for="book in books" 
        :key="book.id" 
        class="book-card"
      >
 
        <div class="book-details">
          <h3 class="book-title" @click="viewBook(book.id)">{{ book.title }}</h3>
          <p class="book-author">{{ book.author }}</p>
          
          <div class="book-actions">
            <button @click="viewBook(book.id)" class="action-btn view">
              <i class="fas fa-eye"></i> View
            </button>
            <button @click="removeFromCollection(book.id)" class="action-btn remove">
              <i class="fas fa-trash-alt"></i> Remove
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="showAddBooksModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showAddBooksModal = false">&times;</span>
        <h2>Add Books to Collection</h2>
        
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            placeholder="Search books by title or author..."
            @input="searchBooks"
          >
          <i class="fas fa-search"></i>
        </div>
        
        <div v-if="searchLoading" class="loading">
          <i class="fas fa-spinner fa-spin"></i> Searching books...
        </div>
        
        <div v-else-if="searchError" class="error-alert">
          <i class="fas fa-exclamation-circle"></i> {{ searchError }}
        </div>
        
        <div v-else class="search-results">
          <div 
            v-for="book in searchResults" 
            :key="book.id" 
            class="book-result"
          >
            <div class="book-info">
              <div class="book-cover-small">
                <img 
                  v-if="book.cover" 
                  :src="book.cover" 
                  alt="Book cover"
                >
                <div v-else class="placeholder-cover-small">
                  <i class="fas fa-book"></i>
                </div>
              </div>
              <div class="book-text">
                <h4>{{ book.title }}</h4>
                <p>{{ book.author }}</p>
              </div>
            </div>
            
            <button 
              @click="addBook(book.id)"
              :disabled="collectionBooks.has(book.id)"
              class="add-btn"
            >
              <i class="fas fa-plus"></i>
              {{ collectionBooks.has(book.id) ? 'Added' : 'Add' }}
            </button>
          </div>
        </div>
        
        <div class="modal-actions">
          <button class="secondary-btn" @click="showAddBooksModal = false">
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBooksStore } from '@/store/books'
import { useCollectionsStore } from '@/store/collections'

const route = useRoute()
const router = useRouter()
const collectionsStore = useCollectionsStore()
const booksStore = useBooksStore()

const collection = ref({
  id: route.params.id,
  title: '',
  description: '',
  bookCount: 0,
  createdAt: new Date(),
  isPrivate: false
})
const books = ref([])
const loading = ref(true)
const showAddBooksModal = ref(false)
const searchQuery = ref('')
const searchResults = ref([])
const searchLoading = ref(false)
const searchError = ref(null)

const collectionBooks = computed(() => {
  return new Set(books.value.map(book => book.id))
})

onMounted(async () => {
  await loadCollection()
})

async function loadCollection() {
  loading.value = true
  try {
    const data = await collectionsStore.fetchCollection(route.params.id)
    collection.value = data.collection
    books.value = data.collection.books
  } catch (error) {
    console.error('Error loading collection:', error)
  } finally {
    loading.value = false
  }
}

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

function viewBook(bookId) {
  router.push({ name: 'bookProfile', params: { id: bookId } })
}

async function removeFromCollection(bookId) {
  if (confirm('Remove this book from the collection?')) {
    try {
      await collectionsStore.removeBookFromCollection(collection.value.id, bookId)
      books.value = books.value.filter(book => book.id !== bookId)
    } catch (error) {
      console.error('Error removing book from collection:', error)
    }
  }
}

function addBooksToCollection() {
  showAddBooksModal.value = true
  searchQuery.value = ''
  searchResults.value = []
  searchError.value = null
}

async function searchBooks() {
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    return
  }
  
  searchLoading.value = true
  searchError.value = null
  
  try {
    const allBooks = await booksStore.books
    searchResults.value = allBooks.filter(book =>
      (book.title ?? '').toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (book.author ?? '').toLowerCase().includes(searchQuery.value.toLowerCase())
    )
    .slice(0, 10)
  } catch (error) {
    searchError.value = 'Failed to search books'
    console.error(error)
  } finally {
    searchLoading.value = false
  }
}

async function addBook(bookId) {
  try {
    await collectionsStore.addBookToCollection(collection.value.id, bookId)
    // Add to local state
    const bookToAdd = searchResults.value.find(b => b.id === bookId)
    if (bookToAdd) {
      books.value.push(bookToAdd)
    }
  } catch (error) {
    console.error('Error adding book to collection:', error)
  }
}
</script>

<style scoped>
.page-header {
  margin-bottom: 40px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.header-top {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.private-badge {
  background: rgba(118, 75, 162, 0.1);
  color: #764ba2;
  border: none;
  padding: 6px 15px;
  border-radius: 20px;
  font-size: 14px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
}

.page-subtitle {
  color: #666;
  text-align: left;
  font-size: 18px;
  margin-bottom: 25px;
  line-height: 1.6;
}

.collection-meta {
  display: flex;
  gap: 25px;
  margin: 20px 0;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8f9ff;
  padding: 10px 20px;
  border-radius: 10px;
  font-size: 16px;
}

.meta-item i {
  color: #667eea;
}

.collection-actions {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.action-btn {
  padding: 12px 25px;
  border-radius: 30px;
  cursor: pointer;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  border: none;
  transition: all 0.3s;
}

.action-btn.primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.action-btn.primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.action-btn {
  background: white;
  color: #764ba2;
  border: 1px solid #ddd;
}

.action-btn:hover {
  background: #f8f9ff;
  border-color: #764ba2;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #764ba2;
  font-size: 18px;
}

.loading i {
  margin-right: 10px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 50px 20px;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
  max-width: 500px;
  margin: 0 auto;
}

.empty-illustration {
  width: 120px;
  height: 120px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 25px;
  color: white;
  font-size: 60px;
}

.empty-state h3 {
  font-size: 24px;
  color: #764ba2;
  margin-bottom: 15px;
}

.empty-state p {
  color: #666;
  margin-bottom: 25px;
  font-size: 16px;
}

.primary-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 30px;
  border-radius: 30px;
  cursor: pointer;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.primary-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.book-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
}

.book-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
}

.book-cover {
  height: 200px;
  overflow: hidden;
  cursor: pointer;
}

.book-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.book-cover:hover img {
  transform: scale(1.05);
}

.placeholder-cover {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 60px;
}

.book-details {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.book-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 5px;
  cursor: pointer;
  transition: color 0.2s;
}

.book-title:hover {
  color: #667eea;
}

.book-author {
  color: #666;
  margin: 0 0 15px;
  font-size: 15px;
}

.book-actions {
  display: flex;
  gap: 10px;
  margin-top: auto;
}

.book-actions button {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  border: none;
  transition: all 0.2s;
}

.book-actions button.view {
  background: #f0f7ff;
  color: #667eea;
}

.book-actions button.view:hover {
  background: #e1eeff;
}

.book-actions button.remove {
  background: #fff0f0;
  color: #ff6b6b;
}

.book-actions button.remove:hover {
  background: #ffe1e1;
}

/* Add Books Modal */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 20px;
  width: 100%;
  max-width: 700px;
  position: relative;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
}

.close {
  position: absolute;
  top: 20px;
  right: 20px;
  font-size: 28px;
  cursor: pointer;
  color: #666;
  transition: color 0.2s;
}

.close:hover {
  color: #333;
}

.search-box {
  position: relative;
  margin: 20px 0 30px;
}

.search-box input {
  width: 100%;
  padding: 14px 20px 14px 50px;
  border: 1px solid #ddd;
  border-radius: 30px;
  font-size: 16px;
  transition: all 0.3s;
}

.search-box input:focus {
  border-color: #667eea;
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.search-box i {
  position: absolute;
  left: 20px;
  top: 50%;
  transform: translateY(-50%);
  color: #667eea;
  font-size: 18px;
}

.error-alert {
  background: #ffebee;
  border-left: 4px solid #f44336;
  padding: 15px 20px;
  border-radius: 8px;
  margin: 20px 0;
  display: flex;
  align-items: center;
  gap: 15px;
}

.error-alert i {
  color: #f44336;
  font-size: 24px;
}

.search-results {
  max-height: 400px;
  overflow-y: auto;
  margin: 20px 0;
}

.book-result {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #eee;
  transition: background 0.2s;
}

.book-result:hover {
  background: #f9f9ff;
}

.book-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.book-cover-small {
  width: 60px;
  height: 90px;
  overflow: hidden;
  border-radius: 5px;
  flex-shrink: 0;
}

.book-cover-small img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.placeholder-cover-small {
  width: 100%;
  height: 100%;
  background: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #764ba2;
  font-size: 24px;
}

.book-text {
  flex-grow: 1;
}

.book-text h4 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.book-text p {
  margin: 5px 0 0;
  color: #666;
  font-size: 14px;
}

.add-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
  transition: all 0.2s;
}

.add-btn:disabled {
  background: #cccccc;
  cursor: not-allowed;
  transform: none;
}

.add-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.secondary-btn {
  background: #f0f0f0;
  color: #333;
  border: none;
  padding: 12px 25px;
  border-radius: 30px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s;
}

.secondary-btn:hover {
  background: #e0e0e0;
}
</style>