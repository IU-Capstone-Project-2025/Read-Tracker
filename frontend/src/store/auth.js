import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

const API_URL = 'http://localhost:8000'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('authToken') || null,
    loading: false,
    error: null
  }),
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  actions: {
    async register(userData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${API_URL}/auth/register`, {
          email: userData.email,
          password: userData.password
        })
        
        if (response.data.status === 'success') {
          return true
        } else {
          throw new Error(response.data.message || 'Registration failed')
        }
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
        const response = await axios.post(`${API_URL}/auth/login`, {
          mail: credentials.email,
          password: credentials.password
        })
        
        if (response.data.status === 'success') {
          this.token = response.data.token
          localStorage.setItem('authToken', this.token)
          
          // Fetch user profile
          await this.fetchProfile()
          
          return true
        } else {
          throw new Error(response.data.message || 'Login failed')
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
        const response = await axios.get(`${API_URL}/auth/profile`, {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        
        if (response.data.status === 'success') {
          this.user = response.data.data
          return this.user
        } else {
          throw new Error(response.data.message || 'Failed to fetch profile')
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Failed to fetch profile'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('authToken')
      useRouter().push('/login')
    },
    
    async resetPasswordRequest(email) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${API_URL}/auth/forgot_password`, {
          mail: email
        })
        
        if (response.data.status === 'success') {
          return true
        } else {
          throw new Error(response.data.message || 'Password reset request failed')
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Password reset request failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async resetPassword(token, newPassword) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${API_URL}/auth/reset_password`, {
          token: token,
          new_password: newPassword
        })
        
        if (response.data.status === 'success') {
          return true
        } else {
          throw new Error(response.data.message || 'Password reset failed')
        }
      } catch (error) {
        this.error = error.response?.data?.message || error.message || 'Password reset failed'
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})