import { mount } from '@vue/test-utils'
import CollectionsPage from '@/components/pages/CollectionsPage.vue'
import { useCollectionsStore } from '@/store/collections'
import { nextTick } from 'vue'

jest.mock('@/store/collections', () => ({
  useCollectionsStore: jest.fn()
}))

describe('CollectionsPage', () => {
  let mockStore
  let mockRouter

  beforeEach(() => {
    mockStore = {
      collections: [],
      loading: false,
      error: null,
      fetchCollections: jest.fn(),
      createCollection: jest.fn(),
      deleteCollection: jest.fn()
    }
    
    mockRouter = {
      push: jest.fn()
    }
    
    useCollectionsStore.mockReturnValue(mockStore)
  })

  it('shows empty state', () => {
    const wrapper = mount(CollectionsPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    expect(wrapper.find('.empty-state').exists()).toBe(true)
    expect(wrapper.text()).toContain('No collections yet')
  })

  it('displays collections', async () => {
    mockStore.collections = [
      { id: 1, title: 'Fantasy', bookCount: 5, description: 'Magical books', isPrivate: false },
      { id: 2, title: 'Sci-Fi', bookCount: 3, description: 'Space adventures', isPrivate: true }
    ]
    
    const wrapper = mount(CollectionsPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    await nextTick()
    
    expect(wrapper.findAll('.collection-card')).toHaveLength(2)
    expect(wrapper.text()).toContain('Fantasy')
    expect(wrapper.text()).toContain('Sci-Fi')
    expect(wrapper.text()).toContain('Private')
  })

  it('opens create modal', async () => {
    const wrapper = mount(CollectionsPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    await wrapper.find('.create-btn').trigger('click')
    
    expect(wrapper.vm.showCreateModal).toBe(true)
    expect(wrapper.find('.modal').exists()).toBe(true)
  })

  it('creates a new collection', async () => {
    const wrapper = mount(CollectionsPage, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    wrapper.vm.showCreateModal = true
    await nextTick()
    
    // Fill form
    await wrapper.find('input[type="text"]').setValue('New Collection')
    await wrapper.find('textarea').setValue('Test description')
    await wrapper.find('input[type="checkbox"]').setChecked(true)
    
    // Submit form
    await wrapper.find('form').trigger('submit')
    
    expect(mockStore.createCollection).toHaveBeenCalledWith({
      title: 'New Collection',
      description: 'Test description',
      isPrivate: true
    })
  })
})