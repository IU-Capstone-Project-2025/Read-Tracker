import { defineStore } from 'pinia'
import { fetchCollections, createCollection } from '@/api/collections'

export const useCollectionsStore = defineStore('collections', {
  state: () => ({
    collections: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchCollections() {
      this.loading = true
      try {
        this.collections = await fetchCollections()
        this.error = null
      } catch (error) {
        this.error = error.message
        console.error('Error fetching collections:', error)
      } finally {
        this.loading = false
      }
    },
    async addCollection(collectionData) {
      try {
        const newCollection = await createCollection(collectionData)
        this.collections.push(newCollection)
        return newCollection
      } catch (error) {
        console.error('Error adding collection:', error)
        throw error
      }
    }
  }
})