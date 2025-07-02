<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <h1>Create Account</h1>
        <p>Join our reading community today</p>
      </div>
      
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label>Email Address</label>
          <input 
            type="email" 
            v-model="userData.email" 
            placeholder="Enter your email"
            required
          >
          <i class="fas fa-envelope"></i>
        </div>
        
        <div class="form-group">
          <label>Password</label>
          <input 
            type="password" 
            v-model="userData.password" 
            placeholder="Create a password"
            required
          >
          <i class="fas fa-lock"></i>
        </div>
        
        <div class="form-group">
          <label>Confirm Password</label>
          <input 
            type="password" 
            v-model="userData.confirmPassword" 
            placeholder="Confirm your password"
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
          <span v-if="!loading">Create Account</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>
        
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>
      </form>
      
      <div class="auth-footer">
        <p>Already have an account? <router-link to="/login">Sign In</router-link></p>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

const userData = ref({
  email: '',
  password: '',
  confirmPassword: ''
})
const loading = ref(false)
const error = ref(null)

const passwordValid = computed(() => {
  return {
    length: userData.value.password.length >= 8,
    upper: /[A-Z]/.test(userData.value.password),
    lower: /[a-z]/.test(userData.value.password),
    number: /[0-9]/.test(userData.value.password)
  }
})

async function handleRegister() {
  // Validate password match
  if (userData.value.password !== userData.value.confirmPassword) {
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
  
  try {
    const success = await authStore.register({
      email: userData.value.email,
      password: userData.value.password
    })
    
    if (success) {
      // Redirect to login after successful registration
      router.push('/login')
    }
  } catch (err) {
    error.value = err.message || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.password-rules {
  background: #f8f9ff;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 25px;
}

.password-rules p {
  margin: 0 0 10px;
  font-weight: 500;
  color: #555;
}

.password-rules ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.password-rules li {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.password-rules li:before {
  content: '✓';
  display: inline-block;
  width: 20px;
  height: 20px;
  background: #eee;
  border-radius: 50%;
  text-align: center;
  line-height: 20px;
  font-size: 12px;
  color: #666;
}

.password-rules li.valid:before {
  background: #4caf50;
  color: white;
}
</style>