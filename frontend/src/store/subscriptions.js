import { defineStore } from 'pinia'
import {
  apiGetAllReviews
} from '@/api/subscriptions'


export const useSubscriptionsStore = defineStore('subscriptions', {
  state: () => ({
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
  }
})