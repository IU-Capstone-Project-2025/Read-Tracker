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

    async fetchSubscriptions() {
      try {
        this.loading = true
        const response = await getUserSubscriptions(this.userId)
        this.subscriptions = response.data || []
      } catch (e) {
        console.error('fetchSubscriptions error:', e)
        throw e
      } finally {
        this.loading = false
      }
    },
    
    async subscribe(publisherId) {
      try {
        const response = await subscribeToUser(publisherId, this.userId)
        await this.fetchSubscriptions()
        return publisherId
      } catch (e) {
        console.error('subscribe error:', e)
        throw e
      }
    },
    
    async unsubscribe(publisherId) {
      try {
        await unsubscribeFromUser(publisherId, this.userId)
        this.subscriptions = this.subscriptions.filter(
          sub => sub.id !== publisherId
        )
      } catch (e) {
        console.error('unsubscribe error:', e)
        throw e
      }
    },
    
    isSubscribedTo(userId) {
      return this.subscriptions.some(sub => sub.id === userId)
    },
    
    getSubscriptionId(userId) {
      const subscription = this.subscriptions.find(sub => sub.id === userId)
      return subscription ? subscription.id : null
    }
  }
})