import { defineStore } from 'pinia'
import { 
  subscribeToUser, 
  unsubscribeFromUser, 
  getUserSubscriptions,
  apiGetAllReviews
} from '@/api/subscriptions'

export const useSubscriptionsStore = defineStore('subscriptions', {
  state: () => ({
    subscriptions: [],
    loading: false,
    reviews: [],
    userId: null
  }),
  
  actions: {
    async init(userId) {
      this.userId = userId
    },

    async getAllReviews() {
      try {
        const data = await apiGetAllReviews(this.userId)
        this.reviews = data.data || []
      } catch (e) {
        console.error('getAllReviews error:', e)
      }
    },

    async fetchSubscriptions(userId) {
      try {
        this.loading = true
        const response = await getUserSubscriptions(userId)
        this.subscriptions = response.data.map(sub => sub.id) || []
      } catch (e) {
        console.error('fetchSubscriptions error:', e)
        throw e
      } finally {
        this.loading = false
      }
    },
    
    async subscribe(publisherId, subscriberId) {
      try {
        await subscribeToUser(publisherId, subscriberId)
        if (!this.subscriptions.includes(publisherId)) {
          this.subscriptions.push(publisherId)
        }
      } catch (e) {
        console.error('subscribe error:', e)
        throw e
      }
    },
    
    async unsubscribe(publisherId, subscriberId) {
      try {
        await unsubscribeFromUser(publisherId, subscriberId)
        this.subscriptions = this.subscriptions.filter(id => id !== publisherId)
      } catch (e) {
        console.error('unsubscribe error:', e)
        throw e
      }
    },
    
    isSubscribedTo(userId) {
      return this.subscriptions.includes(userId)
    }
  }
})