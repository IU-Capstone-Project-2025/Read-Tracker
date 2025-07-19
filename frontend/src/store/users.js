import { defineStore } from 'pinia'
import { getUserProfileById } from '@/api/users'

export const useUsersStore = defineStore('users', {
  state: () => ({
    userProfiles: {}
  }),
  actions: {
    async fetchUserProfile(userId) {
      if (this.userProfiles[userId]) {
        return this.userProfiles[userId]
      }
      
      try {
        const response = await getUserProfileById(userId)
        if (response.status === 'success') {
          this.userProfiles[userId] = response.data
          return response.data
        }
      } catch (error) {
        console.error('Failed to fetch user profile:', error)
      }
      return null
    }
  }
})