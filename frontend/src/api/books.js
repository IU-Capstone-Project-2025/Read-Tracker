import axios from 'axios'
import config from '@/runtimeConfig'
import { useAuthStore } from '@/store/auth'

// Create axios instance with base URL
const api = axios.create({
  baseURL: config.api.baseUrl
})

api.interceptors.request.use(config => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

export async function fetchBooks() {
  try {
    console.log('[API] Fetching books...')
    const response = await api.get('/books/')
    if (response.data.status === 'success') {
      console.log(`[API] Successfully fetched ${response.data.data.length} books`)
      return response.data.data.map(book => ({
        id: book.id,
        title: book.title,
        author: book.author,
        language: book.language,
        description: book.description,
        cover: book.cover || null,
        status: book.status || 'not started'
      }))
    } else {
      const errorMsg = response.data.message || 'Failed to fetch books. Please try again later.'
      console.error('[API] fetchBooks error:', errorMsg)
      throw new Error(errorMsg)
    }
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load books. Please check your connection and try again.'
    console.error('[API] fetchBooks exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export async function fetchBook(bookId) {
  try {
    console.log(`[API] Fetching book with ID: ${bookId}`)
    const response = await api.get(`/books/${bookId}`)
    if (response.data.status === 'success') {
      console.log(`[API] Successfully fetched book: ${response.data.data.title}`)
      const book = response.data.data
      return {
        id: book.id,
        title: book.title,
        author: book.author,
        language: book.language,
        description: book.description,
        cover: book.cover || null,
        status: book.status || 'not started'
      }
    } else {
      const errorMsg = response.data.message || 'Failed to fetch book details. Please try again.'
      console.error('[API] fetchBook error:', errorMsg)
      throw new Error(errorMsg)
    }
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load book details. The book may not exist or you may not have access.'
    console.error('[API] fetchBook exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export async function createBook(bookData) {
  try {
    const response = await api.post('/books/', {
      title: bookData.title,
      author: bookData.author,
      language: bookData.language,
      description: bookData.description
    })
    
    if (response.data.status === 'success') {
      return {
        id: response.data.data.id,
        title: response.data.data.title,
        author: response.data.data.author,
        language: response.data.data.language,
        description: response.data.data.description,
        cover: response.data.data.cover || null,
        status: response.data.data.status || 'not started'
      }
    } else {
      throw new Error(response.data.message || 'Failed to create book')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function updateBook(bookId, bookData) {
  try {
    const response = await api.put(`/books/${bookId}`, {
      title: bookData.title,
      author: bookData.author,
      language: bookData.language,
      description: bookData.description,
      status: bookData.status
    })
    
    if (response.data.status === 'success') {
      return response.data.data
    } else {
      throw new Error(response.data.message || 'Failed to update book')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function deleteBook(bookId) {
  try {
    const response = await api.delete(`/books/${bookId}`)
    if (response.data.status === 'success') {
      return true
    } else {
      throw new Error(response.data.message || 'Failed to delete book')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function fetchBookReviews(bookId) {
  try {
    const response = await api.get(`/books/${bookId}/reviews`)
    if (response.data.status === 'success') {
      return response.data.data
    } else {
      throw new Error(response.data.message || 'Failed to fetch book reviews')
    }
  } catch (error) {
    console.error('API error:', error)
    return []
  }
}

export async function fetchBookNotes(bookId) {
  try {
    const response = await api.get(`/books/${bookId}/notes`)
    if (response.data.status === 'success') {
      return response.data.data
    } else {
      throw new Error(response.data.message || 'Failed to fetch book notes')
    }
  } catch (error) {
    console.error('API error:', error)
    return []
  }
}

export async function addBookNote(bookId, noteData) {
  try {
    const response = await api.post(`/books/${bookId}/notes`, {
      content_type: noteData.contentType,
      text: noteData.text
    })
    
    if (response.data.status === 'success') {
      return response.data.data
    } else {
      throw new Error(response.data.message || 'Failed to add note')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}