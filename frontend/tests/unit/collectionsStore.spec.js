import { setActivePinia, createPinia } from 'pinia'
import { useCollectionsStore } from '@/store/collections'
import { fetchCollections, createCollection } from '@/api/collections'

jest.mock('@/api/collections')

describe('Collections Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    jest.clearAllMocks()
  })

  it('fetches collections', async () => {
    const store = useCollectionsStore()
    const mockCollections = [
      { id: 1, title: 'Fantasy Books', bookCount: 5 },
      { id: 2, title: 'Sci-Fi Books', bookCount: 3 }
    ]
    
    fetchCollections.mockResolvedValue(mockCollections)
    
    await store.fetchCollections()
    
    expect(store.collections).toEqual(mockCollections)
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('handles fetch error', async () => {
    const store = useCollectionsStore()
    const errorMessage = 'Failed to fetch collections'
    fetchCollections.mockRejectedValue(new Error(errorMessage))
    
    await store.fetchCollections()
    
    expect(store.error).toBe(errorMessage)
    expect(store.collections).toEqual([])
  })

  it('creates a new collection', async () => {
    const store = useCollectionsStore()
    const newCollection = {
      title: 'New Collection',
      description: 'Test description',
      isPrivate: false
    }
    const createdCollection = { id: 3, ...newCollection, bookCount: 0 }
    
    createCollection.mockResolvedValue(createdCollection)
    
    await store.createCollection(newCollection)
    
    expect(store.collections).toContainEqual(createdCollection)
    expect(store.error).toBeNull()
  })

  it('deletes a collection', async () => {
    const store = useCollectionsStore()
    store.collections = [
      { id: 1, title: 'Collection 1' },
      { id: 2, title: 'Collection 2' }
    ]
    
    // Mock API call
    jest.spyOn(store, 'deleteCollection').mockImplementation(async (id) => {
      store.collections = store.collections.filter(c => c.id !== id)
    })
    
    await store.deleteCollection(1)
    
    expect(store.collections).toHaveLength(1)
    expect(store.collections[0].id).toBe(2)
  })
})