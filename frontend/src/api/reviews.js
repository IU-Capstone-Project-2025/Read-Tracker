import axios from 'axios'
import config from '@/runtimeConfig'
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

export const getMyReviews = async () => {
  try {
    console.log('[API] Fetching user reviews...')
    const response = await api.get('/me/reviews')
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to load your reviews. Please try again.'
      console.error('[API] getMyReviews error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Successfully fetched ${response.data.data.length} reviews`)
    return response.data.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load reviews. Please check your connection and try again.'
    console.error('[API] getMyReviews exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const getBookReviews = async (bookId) => {
  try {
    console.log(`[API] Fetching reviews for book ID: ${bookId}`)
    const response = await api.get(`/books/${bookId}/reviews`)
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to load book reviews. Please try again.'
      console.error('[API] getBookReviews error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Successfully fetched ${response.data.data.length} reviews for book ID: ${bookId}`)
    return response.data.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load book reviews. The book may not exist or you may not have access.'
    console.error('[API] getBookReviews exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const createReview = async (bookId, review) => {
  try {
    console.log(`[API] Creating review for book ID: ${bookId}`)
    const response = await api.post(`/me/reviews/${bookId}`, review)
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to create review. Please try again.'
      console.error('[API] createReview error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Review created successfully for book ID: ${bookId}`)
    return response.data.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to create review. Please check your connection and try again.'
    console.error('[API] createReview exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const updateReview = async (bookId, review) => {
  try {
    console.log(`[API] Updating review for book ID: ${bookId}`)
    const response = await api.put(`/me/reviews/${bookId}`, review)
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to update review. Please try again.'
      console.error('[API] updateReview error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Review updated successfully for book ID: ${bookId}`)
    return response.data.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to update review. Please check your connection and try again.'
    console.error('[API] updateReview exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const deleteReview = async (bookId) => {
  try {
    console.log(`[API] Deleting review for book ID: ${bookId}`)
    const response = await api.delete(`/me/reviews/${bookId}`)
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to delete review. Please try again.'
      console.error('[API] deleteReview error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Review deleted successfully for book ID: ${bookId}`)
    return response.data.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to delete review. Please check your connection and try again.'
    console.error('[API] deleteReview exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}
