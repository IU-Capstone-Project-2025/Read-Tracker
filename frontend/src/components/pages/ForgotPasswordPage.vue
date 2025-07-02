<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <h1>Reset Password</h1>
        <p>Enter your email to receive a password reset link</p>
      </div>
      
      <form @submit.prevent="handleResetRequest" class="auth-form">
        <div class="form-group">
          <label>Email Address</label>
          <input 
            type="email" 
            v-model="email" 
            placeholder="Enter your email"
            required
          >
          <i class="fas fa-envelope"></i>
        </div>
        
        <button type="submit" class="auth-btn" :disabled="loading">
          <span v-if="!loading">Send Reset Link</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>
        
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>
        
        <div v-if="success" class="success-message">
          <i class="fas fa-check-circle"></i> Password reset link has been sent to your email
        </div>
      </form>
      
      <div class="auth-footer">
        <p>Remember your password? <router-link to="/login">Sign In</router-link></p>
      </div>
    </div>
    
    <div class="auth-decoration">
      <div class="decoration-content">
        <div class="logo">
          <i class="fas fa-book-open"></i>
          <span>ReadTracker</span>
        </div>
        <p>Track your reading, discover new books, and join a community of readers</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

const email = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(false)

async function handleResetRequest() {
  loading.value = true
  error.value = null
  success.value = false
  
  try {
    await authStore.resetPasswordRequest(email.value)
    success.value = true
  } catch (err) {
    error.value = err.message || 'Failed to send reset link'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.success-message {
  background: #e8f5e9;
  color: #4caf50;
  padding: 15px;
  border-radius: 10px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>