<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-header">
        <h1>Welcome Back</h1>
        <p>Sign in to continue your reading journey</p>
      </div>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>Email Address</label>
          <input 
            type="email" 
            v-model="credentials.email" 
            placeholder="Enter your email"
            required
          >
          <i class="fas fa-envelope"></i>
        </div>
        
        <div class="form-group">
          <label>Password</label>
          <input 
            type="password" 
            v-model="credentials.password" 
            placeholder="Enter your password"
            required
          >
          <i class="fas fa-lock"></i>
        </div>
        
        <div class="form-options">
          <router-link to="/forgot-password" class="forgot-link">
            Forgot Password?
          </router-link>
        </div>
        
        <button type="submit" class="auth-btn" :disabled="loading">
          <span v-if="!loading">Sign In</span>
          <i v-else class="fas fa-spinner fa-spin"></i>
        </button>
        
        <div v-if="error" class="error-message">
          <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>
      </form>
      
      <div class="auth-footer">
        <p>Don't have an account? <router-link to="/register">Sign Up</router-link></p>
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
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

const credentials = ref({
  email: '',
  password: ''
})
const loading = ref(false)
const error = ref(null)

async function handleLogin() {
  loading.value = true
  error.value = null
  
  try {
    const success = await authStore.login(credentials.value)
    if (success) {
      router.push('/')
    }
  } catch (err) {
    error.value = err.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  min-height: 100vh;
  background: #f8f9ff;
}

.auth-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 40px;
  max-width: 500px;
  margin: 0 auto;
}

.auth-decoration {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  display: none;
}

@media (min-width: 992px) {
  .auth-decoration {
    display: flex;
  }
}

.decoration-content {
  max-width: 500px;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 30px;
}

.logo i {
  margin-right: 15px;
  font-size: 40px;
}

.decoration-content p {
  font-size: 18px;
  line-height: 1.6;
  opacity: 0.9;
}

.auth-header {
  text-align: center;
  margin-bottom: 40px;
}

.auth-header h1 {
  font-size: 32px;
  color: #764ba2;
  margin-bottom: 10px;
}

.auth-header p {
  color: #666;
  font-size: 18px;
}

.auth-form {
  background: white;
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 25px;
  position: relative;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 14px 20px 14px 50px;
  border: 1px solid #ddd;
  border-radius: 10px;
  font-size: 16px;
  transition: all 0.3s;
}

.form-group input:focus {
  border-color: #667eea;
  outline: none;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.form-group i {
  position: absolute;
  left: 20px;
  top: 40px;
  color: #667eea;
}

.form-options {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 25px;
}

.forgot-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.forgot-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.auth-btn {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
}

.auth-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.error-message {
  background: #ffebee;
  color: #f44336;
  padding: 15px;
  border-radius: 10px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.auth-footer {
  text-align: center;
  margin-top: 30px;
  color: #666;
}

.auth-footer a {
  color: #667eea;
  font-weight: 500;
  text-decoration: none;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>