import axios from 'axios'
import config from '@/runtimeConfig'

const api = axios.create({
  baseURL: config.api.baseUrl
})

export const apiGetAllReviews = async (userId) => {
    try {
    console.log('[API] Fetching user subscription reviews...')
    const response = await api.post('/subscriptions/all_reviews', {
      subscriber_id: userId
    })
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to load your subscription reviews. Please try again.'
      console.error('[API] getAllReviews error:', errorMsg)
      throw new Error(errorMsg)
    }
    console.log(`[API] Successfully fetched ${response.data.data.length} subscription reviews`)
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load subscription reviews. Please check your connection and try again.'
    console.error('[API] getAllReviews exception:', errorMsg, error)
  }
}

export const subscribeToUser = async (publisherId, subscriberId) => {
  try {
    console.log(`[API] Subscribing to user: ${publisherId}`)
    const response = await api.post('/subscriptions/', {
      publisher_id: publisherId,
      subscriber_id: subscriberId
    })
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to subscribe. Please try again.'
      console.error('[API] subscribeToUser error:', errorMsg)
      throw new Error(errorMsg)
    }
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to subscribe. Please check your connection and try again.'
    console.error('[API] subscribeToUser exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const unsubscribeFromUser = async (publisherId, subscriberId) => {
  try {
    console.log(`[API] Unsubscribing from user: ${publisherId}`)
    const response = await api.delete('/subscriptions', {
      data: {
        publisher_id: publisherId,
        subscriber_id: subscriberId
      }
    })
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to unsubscribe. Please try again.'
      console.error('[API] unsubscribeFromUser error:', errorMsg)
      throw new Error(errorMsg)
    }
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to unsubscribe. Please check your connection and try again.'
    console.error('[API] unsubscribeFromUser exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const getUserSubscriptions = async (userId) => {
  try {
    console.log(`[API] Fetching subscriptions for user: ${userId}`)
    const response = await api.post(`/subscriptions/all_subscriptions`, {user_id: userId})
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to load subscriptions. Please try again.'
      console.error('[API] getUserSubscriptions error:', errorMsg)
      throw new Error(errorMsg)
    }
    
    console.log(`[API] Successfully fetched ${response.data.data.length} subscriptions`)
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load subscriptions. Please check your connection and try again.'
    console.error('[API] getUserSubscriptions exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}