import { defineStore } from 'pinia'

const API_BASE = 'http://localhost:8000'

export const useReviewsStore = defineStore('reviews', {
  state: () => ({
    reviews: [],
    editingReviewId: null
  }),

  actions: {
    async fetchMyReviews() {
      try {
        const res = await fetch(`${API_BASE}/me/reviews`)
        if (!res.ok) throw new Error('Failed to fetch my reviews')
        const data = await res.json()
        this.reviews = data.data || []
      } catch (e) {
        console.error('fetchMyReviews error:', e)
      }
    },

    async fetchReviews(bookId) {
      try {
        const res = await fetch(`${API_BASE}/reviews/${bookId}`)
        if (!res.ok) throw new Error('Failed to fetch reviews')
        const data = await res.json()
        this.reviews = data.data || []
      } catch (e) {
        console.error('fetchReviews error:', e)
      }
    },

    async addReview(bookId, newReview) {
      try {
        const res = await fetch(`${API_BASE}/me/reviews/${bookId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            rate: newReview.rate,
            text: newReview.text
          })
        })
        if (!res.ok) throw new Error('Failed to add review')
        await this.fetchMyReviews()
      } catch (e) {
        console.error('addReview error:', e)
      }
    },

    async updateReview(bookId, updatedReview) {
      try {
        const res = await fetch(`${API_BASE}/me/reviews/${bookId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            rate: updatedReview.rate,
            text: updatedReview.text
          })
        })
        if (!res.ok) throw new Error('Failed to update review')
        await this.fetchMyReviews()
      } catch (e) {
        console.error('updateReview error:', e)
      }
    },

    async deleteReview(bookId) {
      try {
        const res = await fetch(`${API_BASE}/me/reviews/${bookId}`, {
          method: 'DELETE'
        })
        if (!res.ok) throw new Error('Failed to delete review')
        await this.fetchMyReviews()
      } catch (e) {
        console.error('deleteReview error:', e)
      }
    },

    getReviewForBook(bookId) {
      return this.reviews.find(r => String(r.book_id) === String(bookId))
    }
  }
})