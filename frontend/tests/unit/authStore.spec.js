import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/store/auth'
import axios from 'axios'

jest.mock('axios')

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('registers a new user', async () => {
    const store = useAuthStore()
    axios.post.mockResolvedValue({
      data: { status: 'success' }
    })
    
    await store.register({
      email: 'test@example.com',
      password: 'Password123!'
    })
    
    expect(axios.post).toHaveBeenCalledWith(
      'http://localhost:8000/auth/register',
      {
        email: 'test@example.com',
        password: 'Password123!'
      }
    )
    expect(store.error).toBeNull()
  })

  it('handles registration error', async () => {
    const store = useAuthStore()
    const errorMessage = 'Email already exists'
    axios.post.mockRejectedValue({
      response: { data: { message: errorMessage } }
    })
    
    try {
      await store.register({
        email: 'test@example.com',
        password: 'Password123!'
      })
    } catch (error) {
      expect(store.error).toBe(errorMessage)
    }
    
    expect(store.loading).toBe(false)
  })

  it('logs in a user', async () => {
    const store = useAuthStore()
    const mockToken = 'test-token-123'
    axios.post.mockResolvedValue({
      data: {
        status: 'success',
        token: mockToken,
        user_id: 'user-123'
      }
    })
    
    await store.login({
      email: 'test@example.com',
      password: 'Password123!'
    })
    
    expect(store.token).toBe(mockToken)
    expect(localStorage.getItem('authToken')).toBe(mockToken)
    expect(store.error).toBeNull()
  })

  it('handles login error', async () => {
    const store = useAuthStore()
    const errorMessage = 'Invalid credentials'
    axios.post.mockRejectedValue({
      response: { data: { message: errorMessage } }
    })
    
    try {
      await store.login({
        email: 'test@example.com',
        password: 'wrongpassword'
      })
    } catch (error) {
      expect(store.error).toBe(errorMessage)
    }
    
    expect(store.loading).toBe(false)
  })

  it('logs out a user', () => {
    const store = useAuthStore()
    store.token = 'test-token'
    localStorage.setItem('authToken', 'test-token')
    
    store.logout()
    
    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(localStorage.getItem('authToken')).toBeNull()
  })

  it('fetches user profile', async () => {
    const store = useAuthStore()
    store.token = 'test-token'
    const mockUser = { id: 'user-123', email: 'test@example.com' }
    axios.get.mockResolvedValue({
      data: {
        status: 'success',
        data: mockUser
      }
    })
    
    await store.fetchProfile()
    
    expect(store.user).toEqual(mockUser)
    expect(axios.get).toHaveBeenCalledWith(
      'http://localhost:8000/auth/profile',
      {
        headers: { Authorization: 'Bearer test-token' }
      }
    )
  })
})