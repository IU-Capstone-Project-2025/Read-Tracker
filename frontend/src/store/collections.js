import { defineStore } from 'pinia'
import { 
  fetchCollections, 
  createCollection, 
  fetchCollection,
  updateCollection,
  deleteCollection,
  addBookToCollection,
  removeBookFromCollection
} from '@/api/collections'

export const useCollectionsStore = defineStore('collections', {
  state: () => ({
    collections: [],
    currentCollection: null,
    loading: false,
    error: null,
    userId: null
  }),
  actions: {
    async init(userId) {
      this.userId = userId
    },
    
    async fetchCollections() {
      this.loading = true
      this.error = null
      try {
        this.collections = await fetchCollections(this.userId)
      } catch (error) {
        this.error = error.message || 'Failed to load collections'
        console.error('Error fetching collections:', error)
      } finally {
        this.loading = false
      }
    },
    
    async fetchCollection(collectionId) {
      this.loading = true
      this.error = null
      try {
        const data = await fetchCollection(collectionId)
        this.currentCollection = data.collection
        return data
      } catch (error) {
        this.error = error.message || 'Failed to load collection'
        console.error('Error fetching collection:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async createCollection(collectionData) {
      this.loading = true
      this.error = null
      try {
        await createCollection(this.userId, collectionData)
        await this.fetchCollections()
      } catch (error) {
        this.error = error.message || 'Failed to create collection'
        console.error('Error creating collection:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async updateCollection(collectionId, updateData) {
      this.loading = true
      this.error = null
      try {
        await updateCollection(collectionId, updateData)
        await this.fetchCollections()
      } catch (error) {
        this.error = error.message || 'Failed to update collection'
        console.error('Error updating collection:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async deleteCollection(collectionId) {
      this.loading = true
      this.error = null
      try {
        await deleteCollection(collectionId)
        await this.fetchCollections()
      } catch (error) {
        this.error = error.message || 'Failed to delete collection'
        console.error('Error deleting collection:', error)
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async addBookToCollection(collectionId, bookId) {
      try {
        await addBookToCollection(collectionId, bookId)
        
        const collection = this.collections.find(c => c.id === collectionId)
        if (collection) {
          collection.bookCount += 1
        }
        
        if (this.currentCollection && this.currentCollection.id === collectionId) {
          this.currentCollection.bookCount += 1
        }
        
        return true
      } catch (error) {
        console.error('Error adding book to collection:', error)
        throw error
      }
    },
    
    async removeBookFromCollection(collectionId, bookId) {
      try {
        await removeBookFromCollection(collectionId, bookId)
        
        const collection = this.collections.find(c => c.id === collectionId)
        if (collection && collection.bookCount > 0) {
          collection.bookCount -= 1
        }
        
        if (this.currentCollection && this.currentCollection.id === collectionId) {
          this.currentCollection.bookCount -= 1
        }
        
        return true
      } catch (error) {
        console.error('Error removing book from collection:', error)
        throw error
      }
    }
  }
})