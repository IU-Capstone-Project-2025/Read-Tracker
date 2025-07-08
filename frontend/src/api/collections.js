import axios from 'axios'
import config from '@/runtimeConfig'

const api = axios.create({
  baseURL: config.api.baseUrl
})

export async function fetchCollections(userId) {
  try {
    console.log('[API] Fetching collections...')
    const response = await api.post('me/collections/all', {
      user_id: userId
    })
    if (response.data.status === 'success') {
      console.log(`[API] Successfully fetched ${response.data.data.length} collections`)
      return response.data.data.map(collection => ({
        id: collection.id,
        title: collection.title,
        userId: collection.user_id,
        description: collection.description,
        createdAt: collection.created_at,
        isPrivate: collection.is_private,
        cover: collection.cover || null,
        books: [],
        bookCount: 0
      }))
    } else {
      const errorMsg = response.data.message || 'Failed to load collections. Please try again later.'
      console.error('[API] fetchCollections error:', errorMsg)
      throw new Error(errorMsg)
    }
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load collections. Please check your connection and try again.'
    console.error('[API] fetchCollections exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export async function fetchCollection(collectionId) {
  try {
    const response = await api.get(`me/collections/${collectionId}`)
    if (response.data.status === 'success') {
      const dataArray = response.data.data
      const data = Array.isArray(dataArray) ? dataArray[0] : dataArray
      return {
        collection: {
          id: data.id,
          title: data.title,
          userId: data.user_id,
          description: data.description,
          bookCount: data.items.length || 0,
          createdAt: data.created_at,
          isPrivate: data.is_private,
          cover: data.cover || null,
          books: data.items || []
        }
      }
    } else {
      throw new Error(response.data.message || 'Failed to fetch collection')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function createCollection(userId, collectionData) {
  try {
    const response = await api.post('me/collections/', {
      user_id: userId,
      title: collectionData.title,
      description: collectionData.description,
      is_private: collectionData.isPrivate || false
    })
    
    if (response.data.status === 'success') {
      return response.data
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
    const response = await api.put(`me/collections/${collectionId}`, {
      title: updateData.title,
      description: updateData.description,
      is_private: updateData.isPrivate,
      cover: updateData.cover
    })
    
    if (response.data.status === 'success') {
      return response.data
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
    const response = await api.delete(`me/collections/${collectionId}`)
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
    const response = await api.post(`me/collections/${collectionId}/${bookId}`, {
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
    const response = await api.delete(`me/collections/${collectionId}/${bookId}`)
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