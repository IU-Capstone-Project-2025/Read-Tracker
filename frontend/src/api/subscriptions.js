import axios from 'axios'
import config from '@/runtimeConfig'

const api = axios.create({
  baseURL: config.api.baseUrl
})

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

export const unsubscribeFromUser = async (subscriptionId) => {
  try {
    console.log(`[API] Unsubscribing from subscription: ${subscriptionId}`)
    const response = await api.delete(`/subscriptions/${subscriptionId}`)
    
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
    const response = await api.get(`/users/${userId}/subscriptions`)
    
    if (response.data.status !== 'success') {
      const errorMsg = response.data.message || 'Failed to load subscriptions. Please try again.'
      console.error('[API] getUserSubscriptions error:', errorMsg)
      throw new Error(errorMsg)
    }
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 
                    'Failed to load subscriptions. Please check your connection and try again.'
    console.error('[API] getUserSubscriptions exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}