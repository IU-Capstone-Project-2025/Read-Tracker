import axios from 'axios'
import config from '@/config'
import { useAuthStore } from '@/store/auth'

// Create axios instance with base URL
const api = axios.create({
  baseURL: config.api.baseUrl
})

// Add request interceptor to include auth token
api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
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
        cover: collection.cover || null,
        userId: collection.user_id
      }))
    } else {
      throw new Error(response.data.message || 'Failed to fetch collections')
    }
  } catch (error) {
    console.error('API error:', error)
    return []
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
          cover: data.cover || null,
          userId: data.user_id
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

export async function createCollection(collectionData) {
  try {
    const response = await api.post('/collections/', {
      title: collectionData.title,
      description: collectionData.description,
      is_private: collectionData.isPrivate || false
    })
    
    if (response.data.status === 'success') {
      const newCollection = response.data.data
      return {
        id: newCollection.collection_id,
        title: newCollection.title,
        description: newCollection.description,
        bookCount: 0,
        createdAt: newCollection.created_at,
        isPrivate: newCollection.is_private,
        cover: newCollection.cover || null,
        userId: newCollection.user_id
      }
    } else {
      throw new Error(response.data.message || 'Failed to create collection')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function updateCollection(collectionId, updateData) {
  try {
    const response = await api.put(`/collections/${collectionId}`, {
      title: updateData.title,
      description: updateData.description,
      is_private: updateData.isPrivate,
      cover: updateData.cover
    })
    
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

export async function fetchPublicCollections(limit = 10, offset = 0, userId = null) {
  try {
    const params = { limit, offset }
    if (userId) params.user_id = userId
    
    const response = await api.get('/explore/collections', { params })
    
    if (response.data.status === 'success') {
      return {
        items: response.data.data.items.map(collection => ({
          id: collection.collection_id,
          title: collection.title,
          description: collection.description,
          bookCount: collection.book_count || 0,
          createdAt: collection.created_at,
          cover: collection.cover || null,
          userId: collection.user_id,
          userName: collection.username
        })),
        pagination: response.data.data.pagination
      }
    } else {
      throw new Error(response.data.message || 'Failed to fetch public collections')
    }
  } catch (error) {
    console.error('API error:', error)
    return { items: [], pagination: { limit, offset, total: 0 } }
  }
}