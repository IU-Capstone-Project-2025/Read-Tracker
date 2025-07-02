<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <h1>Set New Password</h1>
        <p>Create a new password for your account</p>
      </div>
      
      <form @submit.prevent="handleResetPassword" class="auth-form">
        <input type="hidden" v-model="token">
        
        <div class="form-group">
          <label>New Password</label>
          <input 
            type="password" 
            v-model="newPassword" 
            placeholder="Enter new password"
            required
          >
          <i class="fas fa-lock"></i>
        </div>
        
        <div class="form-group">
          <label>Confirm Password</label>
          <input 
            type="password" 
            v-model="confirmPassword" 
            placeholder="Confirm new password"
            required
          >
          <i class="fas fa-lock"></i>
        </div>
        
        <div class="password-rules">
          <p>Password must contain:</p>
          <ul>
            <li :class="{ 'valid': passwordValid.length }">At least 8 characters</li>
            <li :class="{ 'valid': passwordValid.upper }">One uppercase letter</li>
            <li :class="{ 'valid': passwordValid.lower }">One lowercase letter</li>
            <li :class="{ 'valid': passwordValid.number }">One number</li>
          </ul>
        </div>
        
        <button type="submit" class="auth-btn" :disabled="loading">
          <span v-if="!loading">Reset Password</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>
        
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>
        
        <div v-if="success" class="success-message">
          <i class="fas fa-check-circle"></i> Password has been reset successfully
        </div>
      </form>
      
      <div class="auth-footer">
        <p><router-link to="/login">Back to Sign In</router-link></p>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const token = ref(route.query.token || '')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref(null)
const success = ref(false)

const passwordValid = computed(() => {
  return {
    length: newPassword.value.length >= 8,
    upper: /[A-Z]/.test(newPassword.value),
    lower: /[a-z]/.test(newPassword.value),
    number: /[0-9]/.test(newPassword.value)
  }
})

onMounted(() => {
  if (!token.value) {
    error.value = "Invalid reset token"
  }
})

async function handleResetPassword() {
  // Validate token
  if (!token.value) {
    error.value = "Invalid reset token"
    return
  }
  
  // Validate password match
  if (newPassword.value !== confirmPassword.value) {
    error.value = "Passwords do not match"
    return
  }
  
  // Validate password strength
  if (!Object.values(passwordValid.value).every(v => v)) {
    error.value = "Password does not meet requirements"
    return
  }
  
  loading.value = true
  error.value = null
  success.value = false
  
  try {
    await authStore.resetPassword(token.value, newPassword.value)
    success.value = true
    
    // Redirect to login after delay
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (err) {
    error.value = err.message || 'Password reset failed'
  } finally {
    loading.value = false
  }
}
</script>