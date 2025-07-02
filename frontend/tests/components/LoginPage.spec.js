import { mount } from '@vue/test-utils'
import LoginPage from '@/components/pages/LoginPage.vue'
import { useAuthStore } from '@/store/auth'

jest.mock('@/store/auth', () => ({
  useAuthStore: jest.fn()
}))

describe('LoginPage', () => {
  let mockStore
  let mockRouter

  beforeEach(() => {
    mockStore = {
      loading: false,
      error: null,
      login: jest.fn()
    }
    
    mockRouter = {
      push: jest.fn()
    }
    
    useAuthStore.mockReturnValue(mockStore)
  })

  it('renders login form', () => {
    const wrapper = mount(LoginPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.find('input[type="password"]').exists()).toBe(true)
    expect(wrapper.find('button').text()).toBe('Sign In')
  })

  it('submits login form', async () => {
    const wrapper = mount(LoginPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    // Set form values
    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('Password123!')
    await wrapper.find('form').trigger('submit')
    
    expect(mockStore.login).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'Password123!'
    })
  })

  it('shows loading state', async () => {
    mockStore.loading = true
    const wrapper = mount(LoginPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    expect(wrapper.find('button').find('i').classes()).toContain('fa-spinner')
    expect(wrapper.find('button').text()).toContain('')
  })

  it('displays error message', () => {
    mockStore.error = 'Invalid credentials'
    const wrapper = mount(LoginPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    expect(wrapper.find('.error-message').text()).toContain('Invalid credentials')
  })
})