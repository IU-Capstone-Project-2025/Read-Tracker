<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">My Collections</h1>
      <p class="page-subtitle">Organize your books into collections</p>
      <button class="create-btn" @click="showCreateModal = true">
        <i class="fas fa-plus"></i> New Collection
      </button>
    </div>
    
    <div v-if="loading" class="loading">Loading collections...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="collections.length === 0" class="empty-state">
      <i class="fas fa-folder-open"></i>
      <p>No collections yet. Create your first one!</p>
    </div>
    <div v-else class="collections-grid">
      <div 
        v-for="collection in collections" 
        :key="collection.id" 
        class="collection-card"
      >
        <div class="collection-header">
          <i class="fas fa-folder"></i>
          <h3 class="collection-title">{{ collection.name }}</h3>
        </div>
        <div class="collection-body">
          <p>{{ collection.description || 'No description' }}</p>
          <div class="collection-meta">
            <span>{{ collection.bookCount || 0 }} books</span>
            <span>Created: {{ formatDate(collection.createdAt) }}</span>
          </div>
        </div>
        <div class="collection-actions">
          <button @click="viewCollection(collection)">
            <i class="fas fa-eye"></i> View
          </button>
          <button @click="editCollection(collection)">
            <i class="fas fa-edit"></i> Edit
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="showCreateModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="showCreateModal = false">&times;</span>
        <h2>Create New Collection</h2>
        <form @submit.prevent="handleCreateCollection">
          <div class="form-group">
            <label>Name</label>
            <input v-model="newCollection.name" required>
          </div>
          <div class="form-group">
            <label>Description</label>
            <textarea v-model="newCollection.description"></textarea>
          </div>
          <div class="form-actions">
            <button type="button" @click="showCreateModal = false">Cancel</button>
            <button type="submit">Create</button>
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
const newCollection = ref({
  name: '',
  description: ''
})

onMounted(async () => {
  await loadCollections()
})

async function loadCollections() {
  loading.value = true
  try {
    await collectionsStore.fetchCollections()
    collections.value = collectionsStore.collections
  } catch (err) {
    error.value = 'Failed to load collections'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString()
}

async function handleCreateCollection() {
  try {
    await collectionsStore.addCollection(newCollection.value)
    showCreateModal.value = false
    newCollection.value = { name: '', description: '' }
  } catch (err) {
    console.error('Error creating collection:', err)
  }
}

function viewCollection(collection) {
  router.push({ name: 'collectionDetail', params: { id: collection.id } })
}

function editCollection(collection) {
  console.log('Edit collection:', collection)
}
</script>

<style scoped>
.page-header {
  position: relative;
}

.create-btn {
  position: absolute;
  top: 0;
  right: 0;
  background: #764ba2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
}

.collections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
}

.collection-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  flex-direction: column;
}

.collection-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.collection-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.collection-header i {
  font-size: 24px;
}

.collection-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}

.collection-body {
  padding: 20px;
  flex-grow: 1;
}

.collection-body p {
  margin-bottom: 15px;
  color: #555;
}

.collection-meta {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #777;
}

.collection-actions {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}

.collection-actions button {
  background: #f8f9ff;
  border: 1px solid #ddd;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s;
}

.collection-actions button:hover {
  background: #764ba2;
  color: white;
  border-color: #764ba2;
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

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  position: relative;
}

.close {
  position: absolute;
  top: 15px;
  right: 20px;
  font-size: 24px;
  cursor: pointer;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.form-actions button {
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
}

.form-actions button[type="button"] {
  background: #f0f0f0;
  border: none;
}

.form-actions button[type="submit"] {
  background: #764ba2;
  color: white;
  border: none;
}
</style>