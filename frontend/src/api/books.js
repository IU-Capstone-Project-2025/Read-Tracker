import axios from 'axios'
import config from '@/runtimeConfig'

const api = axios.create({
  baseURL: config.api.baseUrl
})

export async function apiFetchBooks() {
  try {
    console.log('[API] Fetching books...')
    const response = await api.get('/books/')
    if (response.data.status === 'success') {
      console.log(`[API] Successfully fetched ${response.data.data.length} books`)
      console.log(`123`)
      console.log('[API] Raw book covers:', response.data.data.map(book => ({
        id: book.id,
        title: book.title,
        cover: book.cover
      })));
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

export async function apiFetchBook(bookId) {
  try {
    console.log(`[API] Fetching book with ID: ${bookId}`)
    const response = await api.get(`/books/${bookId}`)
    if (response.data.status === 'success') {
      console.log(`[API] Successfully fetched book: ${response.data.data.title}`)
      const book = response.data.data
      console.log('[API] Raw book cover:', { id: book.id, title: book.title, cover: book.cover });
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

export async function apiFetchUserBooks(userId) {
  try {
    console.log(`[API] Fetching user books for user`);
    const response = await api.post('/me/books', { user_id: userId });
    if (response.data.status === 'success') {
      console.log(`[API] Successfully fetched ${response.data.data.length} user books`);
      return response.data.data;
    } else {
      const errorMsg = response.data.message || 'Failed to fetch user books';
      console.error('[API] fetchUserBooks error:', errorMsg);
      throw new Error(errorMsg);
    }
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Failed to load user books';
    console.error('[API] fetchUserBooks exception:', errorMsg, error);
    throw new Error(errorMsg);
  }
}