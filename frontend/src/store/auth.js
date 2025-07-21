import { defineStore } from 'pinia'
import { 
  registerUser, 
  loginUser, 
  fetchUserProfile, 
  requestPasswordReset,
  resetPassword,
  updateUserAvatar,
  updateUserPassword,
  updateUserVisibility,
  apiLoadStreaks,
  apiCheckIn
} from '@/api/users'
import { useBooksStore } from './books'
import { useCollectionsStore } from './collections'
import { useNotesStore } from './notes'
import { useReviewsStore } from './reviews'
import { useSubscriptionsStore } from './subscriptions'
import config from '@/runtimeConfig'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem(config.app.authTokenStorageKey) || null,
    loading: false,
    error: null,
    isInitialized: false,
    streaks: [],
    localMarks: JSON.parse('{}'),
    todayMarked: false,
  }),
  getters: {
    isAuthenticated: (state) => state.isInitialized,
    todayMarkedLocal: (state) => {
      const today = new Date().toISOString().slice(0, 10)
      return !!state.localMarks[today]
    }
  },
  actions: {
    async register(userData) {
      this.loading = true
      this.error = null
      try {
        await registerUser({
          username: userData.username,
          email: userData.email,
          password: userData.password
        })
        return true
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Registration failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async login(credentials) {
      this.loading = true
      this.error = null
      try {
        const response = await loginUser(credentials)
        if (response.status === 'success') {
          this.token = response.user_id
          localStorage.setItem(config.app.authTokenStorageKey, this.token)
          await this.fetchProfile()
          return true
        } else {
          throw new Error(response.message || 'Login failed')
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async fetchProfile() {
      this.loading = true
      this.error = null
      try {
        const response = await fetchUserProfile(this.token)
        if (response.status === 'success') {
          const booksStore = useBooksStore()
          const collectionsStore = useCollectionsStore()
          const notesStore = useNotesStore()
          const reviewsStore = useReviewsStore()
          const subscriptionsStore = useSubscriptionsStore()

          this.user = response.data
          this.user.created_at = new Date(this.user.created_at).getFullYear()

          await booksStore.init(this.user.id)
          await collectionsStore.init(this.user.id)
          await notesStore.init(this.user.id)
          await reviewsStore.init(this.user.id)
          await subscriptionsStore.init(this.user.id)

          await Promise.all([
            booksStore.fetchAllBooks(),
            booksStore.fetchUserBooks(this.user.id),
            collectionsStore.fetchCollections(),
            reviewsStore.fetchMyReviews(),
            subscriptionsStore.fetchSubscriptions(this.user.id)
          ])

          await this.loadLocalMarks()
          this.isInitialized = true
        } else {
          throw new Error(response.message || 'Failed to fetch profile')
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Failed to fetch profile'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async logout() {
      this.user = null
      this.token = null
      localStorage.removeItem(config.app.authTokenStorageKey)
      this.isInitialized = false
    },
    
    async requestPasswordReset(email) {
      this.loading = true
      this.error = null
      try {
        await requestPasswordReset(email)
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Password reset request failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async completePasswordReset(token, newPassword) {
      this.loading = true
      this.error = null
      try {
        await resetPassword(token, newPassword)
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Password reset failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async changeAvatar(avatarUrl) {
      if (!this.user) throw new Error('User not authenticated')
      
      this.loading = true
      this.error = null
      try {
        const response = await updateUserAvatar(this.user.id, avatarUrl, this.token)
        if (response.status === 'success') {
          await this.fetchProfile()
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Avatar update failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async changePassword(currentPassword, newPassword) {
      if (!this.user) throw new Error('User not authenticated')
      
      this.loading = true
      this.error = null
      try {
        await updateUserPassword(this.user.id, currentPassword, newPassword, this.token)
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Password change failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async changeVisibility(isVisible) {
      if (!this.user) throw new Error('User not authenticated')
      
      this.loading = true
      this.error = null
      try {
        await updateUserVisibility(this.user.id, isVisible, this.token)
        this.user.isVisible = isVisible 
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Visibility update failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async loadLocalMarks() {
      const marks = JSON.parse(localStorage.getItem('reading_marks') || '{}')
      const today = new Date().toISOString().slice(0, 10)

      this.localMarks = marks
      this.todayMarked = !!marks[today]
    },

    async loadStreaks() {
      try {
        if (!this.user) throw new Error('User not authenticated')
        const data = await apiLoadStreaks(this.user.id)
        this.streaks = data
        return data
      }
      catch (error) {
        throw error
      } 
    },

    async checkIn() {
      try {
        await apiCheckIn(this.user.id)
        const today = new Date().toISOString().slice(0, 10)
        this.localMarks[today] = true
        localStorage.setItem('reading_marks', JSON.stringify(this.localMarks))
        this.todayMarked = true
      }
      catch (error) {
        console.error(error)
        throw error
      }
    }
  }
})