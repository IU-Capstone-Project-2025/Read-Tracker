import axios from 'axios'
import config from '@/runtimeConfig'
import { useAuthStore } from '@/store/auth'

const api = axios.create({
  baseURL: config.api.baseUrl
})

export async function apiFetchBooks() {
  try {
    const response = await api.get('/books/')
    if (response.data.status === 'success') {
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
      throw new Error(response.data.message || 'Failed to fetch books')
    }
  } catch (error) {
    console.error('API error:', error)
    return []
  }
}

export async function apiFetchBook(bookId) {
  try {
    const response = await api.get(`/books/${bookId}`)
    if (response.data.status === 'success') {
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
      throw new Error(response.data.message || 'Failed to fetch book')
    }
  } catch (error) {
    console.error('API error:', error)
    throw error
  }
}

export async function apiCreateBook(bookData) {
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

export async function apiUpdateBook(bookId, bookData) {
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

export async function apiDeleteBook(bookId) {
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