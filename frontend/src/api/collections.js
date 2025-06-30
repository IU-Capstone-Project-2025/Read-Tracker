import axios from 'axios'
import { useAuthStore } from '@/store/auth'

const API_URL = 'http://localhost:8000'

// Create axios instance with auth header
const api = axios.create({
  baseURL: API_URL
})

// Add request interceptor to include auth token
api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

export async function fetchCollections() {
  try {
    const response = await api.get('/collections/')
    if (response.data.status === 'success') {
      return response.data.data.map(collection => ({
        id: collection.collection_id,
        title: collection.title,
        description: collection.description,
        bookCount: collection.book_count || 0,
        createdAt: collection.created_at,
        isPrivate: collection.is_private,
        cover: collection.cover || null
      }))
    } else {
      throw new Error(response.data.message || 'Failed to fetch collections')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function createCollection(collectionData) {
  try {
    const response = await api.post('/collections/', {
      title: collectionData.title,
      description: collectionData.description,
      is_private: collectionData.isPrivate || false
    })
    
    if (response.data.status === 'success') {
      return {
        id: response.data.data.collection_id,
        title: response.data.data.title,
        description: response.data.data.description,
        bookCount: 0,
        createdAt: response.data.data.created_at,
        isPrivate: response.data.data.is_private,
        cover: response.data.data.cover || null
      }
    } else {
      throw new Error(response.data.message || 'Failed to create collection')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function fetchCollection(collectionId) {
  try {
    const response = await api.get(`/collections/${collectionId}`)
    if (response.data.status === 'success') {
      const data = response.data.data
      return {
        collection: {
          id: data.collection_id,
          title: data.title,
          description: data.description,
          bookCount: data.books ? data.books.length : 0,
          createdAt: data.created_at,
          isPrivate: data.is_private,
          userId: data.user_id,
          cover: data.cover || null
        },
        books: data.books || []
      }
    } else {
      throw new Error(response.data.message || 'Failed to fetch collection')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function updateCollection(collectionId, updateData) {
  try {
    const response = await api.put(`/collections/${collectionId}`, updateData)
    if (response.data.status === 'success') {
      return response.data.data
    } else {
      throw new Error(response.data.message || 'Failed to update collection')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function deleteCollection(collectionId) {
  try {
    const response = await api.delete(`/collections/${collectionId}`)
    if (response.data.status === 'success') {
      return true
    } else {
      throw new Error(response.data.message || 'Failed to delete collection')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function addBookToCollection(collectionId, bookId) {
  try {
    const response = await api.post(`/collections/${collectionId}/books`, {
      book_id: bookId
    })
    if (response.data.status === 'success') {
      return true
    } else {
      throw new Error(response.data.message || 'Failed to add book to collection')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function removeBookFromCollection(collectionId, bookId) {
  try {
    const response = await api.delete(`/collections/${collectionId}/books/${bookId}`)
    if (response.data.status === 'success') {
      return true
    } else {
      throw new Error(response.data.message || 'Failed to remove book from collection')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}