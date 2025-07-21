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
          const userProfile = {
            id: response.data.id,
            username: response.data.username || response.data.name,
            email: response.data.email || response.data.mail,
            avatar: response.data.avatar,
            created_at: response.data.created_at
          }
          
          this.userProfiles[userId] = userProfile
          return userProfile
        }
      } catch (error) {
        console.error('Failed to fetch user profile:', error)
      }
      return null
    }
  }
})