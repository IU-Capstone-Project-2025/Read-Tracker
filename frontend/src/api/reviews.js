import axios from 'axios'
import config from '@/runtimeConfig'


const api = axios.create({
  baseURL: config.api.baseUrl
})


export const getMyReviews = async (userId) => {
  try {
    const response = await api.post('/me/reviews', {
      user_id: userId
    })
    return response.data
  } catch (error) {
    console.error('Failed to fetch all reviews:', error)
    throw error
  }
}

export const getBookReviews = async (userId, bookId) => {
  try {
    const response = await api.post(`me/reviews/${bookId}`, {
      user_id: userId,
    })
    return response.data
  } catch (error) {
    console.error(`Failed to fetch reviews for book ${bookId}: `, error)
    throw error
  }
}

export const createReview = async (userId, bookId, rate, review) => {
  try {
    const response = await api.post(`/me/reviews/${bookId}/new`, {
      user_id: userId,
      rate: rate,
      text: review
    })
    return response.data
  } catch (error) {
    console.error(`Failed to create review for book ${bookId}: `, error)
    throw error
  }
}

export const updateReview = async (userId, bookId, rate, review) => {
  try {
    const response = await api.put(`/me/reviews/${bookId}`, {
      user_id: userId,
      rate: rate,
      text: review
    })
    return response.data
  } catch (error) {
    console.error(`Failed to update review for book ${bookId}: `, error)
    throw error
  }
}

export const deleteReview = async (userId, bookId) => {
  try {
    const response = await api.delete(`/me/reviews/${bookId}`, {
      data: {
        user_id: userId
      }
    })
    return response.data
  } catch (error) {
    console.error(`Failed to delete review for book ${bookId}: `, error)
    throw error
  }
}
