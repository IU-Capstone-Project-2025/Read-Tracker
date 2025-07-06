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
    
    <!-- Added decoration panel -->
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
  if (userData.value.password !== userData.value.confirmPassword) {
    error.value = "Passwords do not match"
    return
  }
  
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
/* Added all auth styles */
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