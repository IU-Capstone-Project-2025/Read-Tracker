import axios from 'axios'
import config from '@/runtimeConfig'

const api = axios.create({
  baseURL: config.api.baseUrl
})

export const registerUser = async (userData) => {
  try {
    console.log('[API] Registering new user...')
    const response = await api.post('/auth/register', {
      name: userData.username,
      email: userData.email,
      password: userData.password
    })

    console.log('[API] User registered successfully')
    return response.data
  } catch (error) {
    let errorMsg = 'Registration failed. Please try again.'
    
    if (error.response?.message) {
      if (error.response.message.includes('email')) {
        errorMsg = 'This email is already registered. Please use a different email.'
      } else if (error.response.message.includes('name')) {
        errorMsg = 'This username is already taken. Please choose a different username.'
      } else {
        errorMsg = error.response.message
      }
    }

    console.error('[API] registerUser error:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const loginUser = async (credentials) => {
  try {
    console.log('[API] User login attempt...')
    const response = await api.post('/auth/login', {
      email: credentials.email,
      password: credentials.password
    })

    console.log('[API] User logged in successfully')
    return response.data
  } catch (error) {
    let errorMsg = 'Login failed. Please try again.'

    if (error.response?.status === 401) {
      errorMsg = 'Invalid email or password. Please check your credentials and try again.'
    } else if (error.response?.data?.message) {
      errorMsg = error.response.data.message
    }

    console.error('[API] loginUser error:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const fetchUserProfile = async () => {
  try {
    console.log('[API] Fetching user profile...')
    // Fix: Change to GET request without body
    const response = await api.get('/auth/profile')
    console.log('[API] User profile fetched successfully')
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Failed to fetch profile. Please try again.'
    console.error('[API] fetchUserProfile error:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const requestPasswordReset = async (email) => {
  try {
    console.log('[API] Requesting password reset...')
    const response = await api.post('/auth/forgot_password', {
      email
    })

    console.log('[API] Password reset request sent')
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Failed to request password reset. Please try again.'
    console.error('[API] requestPasswordReset error:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const resetPassword = async (token, newPassword) => {
  try {
    console.log('[API] Resetting password...')
    const response = await api.post('/auth/reset_password', {
      user_id: token,
      new_password: newPassword
    })

    console.log('[API] Password reset successful')
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Password reset failed. Please try again.'
    console.error('[API] resetPassword error:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const updateUserAvatar = async (userId, avatarUrl, token) => {
  try {
    console.log(`[API] Updating avatar for user ID: ${userId}`)
    const response = await api.put(`/users/${userId}/avatar`, {
      avatarUrl
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    console.log('[API] Avatar updated successfully')
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Failed to update avatar. Please try again.'
    console.error('[API] updateUserAvatar error:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const updateUserPassword = async (userId, currentPassword, newPassword, token) => {
  try {
    console.log(`[API] Updating password for user ID: ${userId}`)
    const response = await api.put(`/users/${userId}/password`, {
      curr_password: currentPassword,
      new_password: newPassword
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    console.log('[API] Password updated successfully')
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Failed to update password. Please try again.'
    console.error('[API] updateUserPassword error:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const updateUserVisibility = async (userId, isVisible, token) => {
  try {
    console.log(`[API] Updating visibility for user ID: ${userId}`)
    const response = await api.put(`/users/${userId}/visibility`, {
      isVisible
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    console.log('[API] Visibility updated successfully')
    return response.data
  } catch (error) {
    const errorMsg = error.response?.data?.message || 'Failed to update visibility. Please try again.'
    console.error('[API] updateUserVisibility error:', errorMsg, error)
    throw new Error(errorMsg)
  }
}
