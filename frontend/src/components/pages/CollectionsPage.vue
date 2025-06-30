<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">My Collections</h1>
      <p class="page-subtitle">Organize your books into collections</p>
      <button class="create-btn" @click="showCreateModal = true">
        <i class="fas fa-plus"></i> New Collection
      </button>
    </div>
    
    <div v-if="loading" class="loading">
      <i class="fas fa-spinner fa-spin"></i> Loading collections...
    </div>
    
    <div v-else-if="error" class="error-alert">
      <i class="fas fa-exclamation-circle"></i> {{ error }}
      <button @click="loadCollections">Retry</button>
    </div>
    
    <div v-else-if="collections.length === 0" class="empty-state">
      <div class="empty-illustration">
        <i class="fas fa-folder-open"></i>
      </div>
      <h3>No Collections Yet</h3>
      <p>Start by creating your first collection to organize your books</p>
      <button class="primary-btn" @click="showCreateModal = true">
        <i class="fas fa-plus"></i> Create Collection
      </button>
    </div>
    
    <div v-else class="collections-grid">
      <div 
        v-for="collection in collections" 
        :key="collection.id" 
        class="collection-card"
        @click="viewCollection(collection)"
      >
        <div class="collection-cover" :style="coverStyle(collection)">
          <div class="overlay">
            <h3 class="collection-title">{{ collection.title }}</h3>
            <p class="book-count">{{ collection.bookCount }} books</p>
          </div>
        </div>
        
        <div class="collection-details">
          <p class="description">{{ truncate(collection.description, 100) || 'No description' }}</p>
          
          <div class="meta-info">
            <span class="created-date">
              <i class="fas fa-calendar"></i> {{ formatDate(collection.createdAt) }}
            </span>
            <span v-if="collection.isPrivate" class="private-badge">
              <i class="fas fa-lock"></i> Private
            </span>
          </div>
        </div>
        
        <div class="collection-actions">
          <button @click.stop="editCollection(collection)" class="action-btn edit">
            <i class="fas fa-edit"></i>
          </button>
          <button @click.stop="deleteCollection(collection.id)" class="action-btn delete">
            <i class="fas fa-trash-alt"></i>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Create Collection Modal -->
    <div v-if="showCreateModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showCreateModal = false">&times;</span>
        <h2>Create New Collection</h2>
        
        <form @submit.prevent="handleCreateCollection">
          <div class="form-group">
            <label>Title*</label>
            <input v-model="newCollection.title" required placeholder="Enter collection title">
          </div>
          
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="newCollection.description" placeholder="Enter a brief description"></textarea>
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="newCollection.isPrivate">
              <span class="checkmark"></span>
              Make this collection private
            </label>
          </div>
          
          <div class="form-actions">
            <button type="button" class="secondary-btn" @click="showCreateModal = false">
              Cancel
            </button>
            <button type="submit" class="primary-btn">
              Create Collection
            </button>
          </div>
        </form>
      </div>
    </div>
    
    <!-- Edit Collection Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showEditModal = false">&times;</span>
        <h2>Edit Collection</h2>
        
        <form @submit.prevent="handleUpdateCollection">
          <div class="form-group">
            <label>Title*</label>
            <input v-model="editCollectionData.title" required>
          </div>
          
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="editCollectionData.description"></textarea>
          </div>
          
          <div class="form-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="editCollectionData.isPrivate">
              <span class="checkmark"></span>
              Private Collection
            </label>
          </div>
          
          <div class="form-actions">
            <button type="button" class="secondary-btn" @click="showEditModal = false">
              Cancel
            </button>
            <button type="submit" class="primary-btn">
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCollectionsStore } from '@/store/collections'

const router = useRouter()
const collectionsStore = useCollectionsStore()

const collections = ref([])
const loading = ref(false)
const error = ref(null)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const newCollection = ref({
  title: '',
  description: '',
  isPrivate: false
})
const editCollectionData = ref({
  id: null,
  title: '',
  description: '',
  isPrivate: false
})

onMounted(() => {
  loadCollections()
})

async function loadCollections() {
  loading.value = true
  error.value = null
  try {
    await collectionsStore.fetchCollections()
    collections.value = collectionsStore.collections
  } catch (err) {
    error.value = err.message || 'Failed to load collections'
  } finally {
    loading.value = false
  }
}

function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' }
  return new Date(dateString).toLocaleDateString(undefined, options)
}

function truncate(text, maxLength) {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

function coverStyle(collection) {
  if (collection.cover) {
    return {
      backgroundImage: `url(${collection.cover})`
    }
  }
  return {
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  }
}

async function handleCreateCollection() {
  try {
    await collectionsStore.createCollection(newCollection.value)
    showCreateModal.value = false
    newCollection.value = { 
      title: '', 
      description: '',
      isPrivate: false
    }
  } catch (err) {
    console.error('Error creating collection:', err)
  }
}

function viewCollection(collection) {
  router.push({ name: 'collectionDetail', params: { id: collection.id } })
}

function editCollection(collection) {
  editCollectionData.value = {
    id: collection.id,
    title: collection.title,
    description: collection.description,
    isPrivate: collection.isPrivate
  }
  showEditModal.value = true
}

async function handleUpdateCollection() {
  try {
    await collectionsStore.updateCollection(
      editCollectionData.value.id,
      {
        title: editCollectionData.value.title,
        description: editCollectionData.value.description,
        is_private: editCollectionData.value.isPrivate
      }
    )
    showEditModal.value = false
  } catch (err) {
    console.error('Error updating collection:', err)
  }
}

async function deleteCollection(collectionId) {
  if (confirm('Are you sure you want to delete this collection? This action cannot be undone.')) {
    try {
      await collectionsStore.deleteCollection(collectionId)
    } catch (error) {
      console.error('Error deleting collection:', error)
    }
  }
}
</script>

<style scoped>
.page-header {
  position: relative;
  margin-bottom: 30px;
}

.create-btn {
  position: absolute;
  top: 0;
  right: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 30px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.create-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
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

.error-alert {
  background: #ffebee;
  border-left: 4px solid #f44336;
  padding: 15px 20px;
  border-radius: 8px;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.error-alert i {
  color: #f44336;
  font-size: 24px;
}

.error-alert button {
  margin-left: auto;
  background: #f44336;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
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

.collections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
}

.collection-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  position: relative;
  cursor: pointer;
}

.collection-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
}

.collection-cover {
  height: 200px;
  background-size: cover;
  background-position: center;
  position: relative;
}

.overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
  color: white;
}

.collection-title {
  font-size: 22px;
  font-weight: 700;
  margin: 0 0 5px;
  color: white;
}

.book-count {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
}

.collection-details {
  padding: 20px;
}

.description {
  color: #555;
  margin-bottom: 15px;
  line-height: 1.6;
}

.meta-info {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #777;
}

.created-date {
  display: flex;
  align-items: center;
  gap: 5px;
}

.private-badge {
  background: rgba(118, 75, 162, 0.1);
  color: #764ba2;
  padding: 4px 10px;
  border-radius: 15px;
  display: flex;
  align-items: center;
  gap: 5px;
  font-weight: 500;
}

.collection-actions {
  position: absolute;
  top: 15px;
  right: 15px;
  display: flex;
  gap: 10px;
}

.action-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  cursor: pointer;
  background: white;
  color: #764ba2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.2s;
}

.action-btn:hover {
  transform: scale(1.1);
}

.action-btn.edit {
  background: #667eea;
  color: white;
}

.action-btn.delete {
  background: #ff6b6b;
  color: white;
}

/* Modal Styles */
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
  max-width: 500px;
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

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: #667eea;
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-weight: 500;
}

.checkbox-label input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
}

.checkmark {
  height: 20px;
  width: 20px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-right: 10px;
  position: relative;
  transition: all 0.2s;
}

.checkbox-label input:checked ~ .checkmark {
  background-color: #667eea;
  border-color: #667eea;
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
  left: 7px;
  top: 3px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.checkbox-label input:checked ~ .checkmark:after {
  display: block;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
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