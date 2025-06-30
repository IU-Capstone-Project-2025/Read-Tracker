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
    error: null
  }),
  actions: {
    async fetchCollections() {
      this.loading = true
      this.error = null
      try {
        this.collections = await fetchCollections()
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
        const newCollection = await createCollection(collectionData)
        this.collections.push(newCollection)
        return newCollection
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
        const updatedCollection = await updateCollection(collectionId, updateData)
        
        // Update in collections list
        const index = this.collections.findIndex(c => c.id === collectionId)
        if (index !== -1) {
          this.collections[index] = { 
            ...this.collections[index],
            ...updatedCollection
          }
        }
        
        // Update current collection if it's the one being edited
        if (this.currentCollection && this.currentCollection.id === collectionId) {
          this.currentCollection = { 
            ...this.currentCollection,
            ...updatedCollection
          }
        }
        
        return updatedCollection
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
        this.collections = this.collections.filter(c => c.id !== collectionId)
        if (this.currentCollection && this.currentCollection.id === collectionId) {
          this.currentCollection = null
        }
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
        
        // Update local state
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
        
        // Update local state
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