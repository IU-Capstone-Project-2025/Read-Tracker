import axios from 'axios'
import config from '@/runtimeConfig'

const api = axios.create({
  baseURL: config.api.baseUrl
})

export const registerUser = async (userData) => {
  try {
    const response = await api.post('/auth/register', {
      name: userData.username,
      email: userData.email,
      password: userData.password
    })
    return response.data
  } catch (error) {
    console.error('Registration error:', error)
    throw error
  }
}

export const loginUser = async (credentials) => {
  try {
    const response = await api.post('/auth/login', {
      email: credentials.email,
      password: credentials.password
    })
    return response.data
  } catch (error) {
    console.error('Login error:', error)
    throw error
  }
}

export const fetchUserProfile = async (token) => {
  try {
    const response = await api.post('/auth/profile', {
      user_id: token
    })
    return response.data
  } catch (error) {
    console.error('Profile fetch error:', error)
    throw error
  }
}

export const requestPasswordReset = async (email) => {
  try {
    const response = await api.post('/auth/forgot_password', {
      email: email
    })
    return response.data
  } catch (error) {
    console.error('Password reset request error:', error)
    throw error
  }
}

export const resetPassword = async (token, newPassword) => {
  try {
    const response = await api.post('/auth/reset_password', {
      user_id: token,
      new_password: newPassword
    })
    return response.data
  } catch (error) {
    console.error('Password reset error:', error)
    throw error
  }
}

export const updateUserAvatar = async (userId, avatarUrl, token) => {
  try {
    const response = await api.put(`/users/${userId}/avatar`, {
      avatarUrl
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    return response.data
  } catch (error) {
    console.error('Avatar update error:', error)
    throw error
  }
}

export const updateUserPassword = async (userId, currentPassword, newPassword, token) => {
  try {
    const response = await api.put(`/users/${userId}/password`, {
      curr_password: currentPassword,
      new_password: newPassword
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    return response.data
  } catch (error) {
    console.error('Password update error:', error)
    throw error
  }
}

export const updateUserVisibility = async (userId, isVisible, token) => {
  try {
    const response = await api.put(`/users/${userId}/visibility`, {
      isVisible
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    return response.data
  } catch (error) {
    console.error('Visibility update error:', error)
    throw error
  }
}