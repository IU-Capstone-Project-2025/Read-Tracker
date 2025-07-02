import { mount } from '@vue/test-utils'
import RegistrationPage from '@/components/pages/RegistrationPage.vue'
import { useAuthStore } from '@/store/auth'

jest.mock('@/store/auth', () => ({
  useAuthStore: jest.fn()
}))

describe('RegistrationPage', () => {
  let mockStore
  let mockRouter

  beforeEach(() => {
    mockStore = {
      loading: false,
      error: null,
      register: jest.fn().mockResolvedValue(true)
    }
    
    mockRouter = {
      push: jest.fn()
    }
    
    useAuthStore.mockReturnValue(mockStore)
  })

  it('renders registration form', () => {
    const wrapper = mount(RegistrationPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    expect(wrapper.find('form').exists()).toBe(true)
    expect(wrapper.find('input[type="email"]').exists()).toBe(true)
    expect(wrapper.findAll('input[type="password"]')).toHaveLength(2)
    expect(wrapper.find('button').text()).toBe('Create Account')
  })

  it('validates password strength', async () => {
    const wrapper = mount(RegistrationPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    // Set weak password
    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('weak')
    await wrapper.findAll('input[type="password"]')[1].setValue('weak')
    await wrapper.find('form').trigger('submit')
    
    expect(mockStore.register).not.toHaveBeenCalled()
    expect(wrapper.find('.error-message').text()).toContain('Password does not meet requirements')
  })

  it('submits registration form', async () => {
    const wrapper = mount(RegistrationPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    // Set valid values
    await wrapper.find('input[type="email"]').setValue('test@example.com')
    await wrapper.find('input[type="password"]').setValue('StrongPassword123!')
    await wrapper.findAll('input[type="password"]')[1].setValue('StrongPassword123!')
    await wrapper.find('form').trigger('submit')
    
    expect(mockStore.register).toHaveBeenCalledWith({
      email: 'test@example.com',
      password: 'StrongPassword123!'
    })
    
    // Wait for router redirect
    await wrapper.vm.$nextTick()
    expect(mockRouter.push).toHaveBeenCalledWith('/login')
  })
})