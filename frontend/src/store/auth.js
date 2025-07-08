import { defineStore } from 'pinia'
import { 
  registerUser, 
  loginUser, 
  fetchUserProfile, 
  requestPasswordReset,
  resetPassword,
  updateUserAvatar,
  updateUserPassword,
  updateUserVisibility
} from '@/api/users'
import { useBooksStore } from './books'
import { useCollectionsStore } from './collections'
import { useNotesStore } from './notes'
import { useReviewsStore } from './reviews'
import config from '@/runtimeConfig'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem(config.app.authTokenStorageKey) || null,
    loading: false,
    error: null,
    isInitialized: false
  }),
  getters: {
    isAuthenticated: (state) => !!state.token && state.isInitialized
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
          this.token = response.token
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
        const response = await fetchUserProfile()
        if (response.status === 'success') {
          const booksStore = useBooksStore()
          const collectionsStore = useCollectionsStore()
          const notesStore = useNotesStore()
          const reviewsStore = useReviewsStore()

          this.user = response.data

          await booksStore.init(this.user.id)
          await collectionsStore.init(this.user.id)
          await notesStore.init(this.user.id)
          await reviewsStore.init(this.user.id)

          await Promise.all([
            booksStore.fetchBooks(),
            collectionsStore.fetchCollections(),
            reviewsStore.fetchMyReviews()
          ])
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
    
    async logout(router) {
      this.user = null
      this.token = null
      localStorage.removeItem(config.app.authTokenStorageKey)
      router.push('/login')
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
    }
  }
})
