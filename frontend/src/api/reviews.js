import axios from 'axios'
import config from '@/runtimeConfig'

const api = axios.create({
  baseURL: config.api.baseUrl
})

export const getMyReviews = async (userId) => {
  try {
    console.log('[API] Fetching user reviews...')
    const response = await api.post('/me/reviews', {
      user_id: userId
    })
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to load your reviews. Please try again.'
      console.error('[API] getMyReviews error:', errorMsg)
      throw new Error(errorMsg)
    }
    console.log(`[API] Successfully fetched ${response.data.data.length} reviews`)
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load reviews. Please check your connection and try again.'
    console.error('[API] getMyReviews exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const getBookReviews = async (userId, bookId) => {
  try {
    console.log(`[API] Fetching reviews for book ID: ${bookId}`)
    const response = await api.post(`me/reviews/${bookId}`, {
      user_id: userId,
    })
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to load book reviews. Please try again.'
      console.error('[API] getBookReviews error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Successfully fetched ${response.data.data.length} reviews for book ID: ${bookId}`)
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load book reviews. The book may not exist or you may not have access.'
    console.error('[API] getBookReviews exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const createReview = async (userId, bookId, rate, review) => {
  try {
    console.log(`[API] Creating review for book ID: ${bookId}`)
    const response = await api.post(`/me/reviews/${bookId}/new`, {
      user_id: userId,
      rate: rate,
      text: review
    })
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to create review. Please try again.'
      console.error('[API] createReview error:', errorMsg)
      throw new Error(errorMsg)
    }
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to create review. Please check your connection and try again.'
    console.error('[API] createReview exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const updateReview = async (userId, bookId, rate, review) => {
  try {
    console.log(`[API] Updating review for book ID: ${bookId}`)
    const response = await api.put(`/me/reviews/${bookId}`, {
      user_id: userId,
      rate: rate,
      text: review
    })
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to update review. Please try again.'
      console.error('[API] updateReview error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Review updated successfully for book ID: ${bookId}`)
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to update review. Please check your connection and try again.'
    console.error('[API] updateReview exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const deleteReview = async (userId, bookId) => {
  try {
    console.log(`[API] Deleting review for book ID: ${bookId}`)
    const response = await api.delete(`/me/reviews/${bookId}`, {
      data: {
        user_id: userId
      }
    })
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to delete review. Please try again.'
      console.error('[API] deleteReview error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Review deleted successfully for book ID: ${bookId}`)
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to delete review. Please check your connection and try again.'
    console.error('[API] deleteReview exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}
