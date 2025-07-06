import { defineStore } from 'pinia'
import {
  getMyReviews,
  getBookReviews,
  createReview,
  updateReview,
  deleteReview
} from '@/api/reviews'


export const useReviewsStore = defineStore('reviews', {
  state: () => ({
    reviews: [],
    editingReviewId: null,
    userId: null
  }),

  actions: {
    async init(userId) {
      this.userId = userId
    },

    async fetchMyReviews() {
      try {
        const data = await getMyReviews(this.userId)
        this.reviews = data.data || []
      } catch (e) {
        console.error('fetchMyReviews error:', e)
      }
    },

    async fetchReviews(bookId) {
      try {
        const data = await getBookReviews(this.userId, bookId)
        this.reviews = data.data || []
      } catch (e) {
        console.error('fetchReviews error:', e)
      }
    },

    async addReview(newReview) {
      try {
        await createReview(this.userId, newReview.book_id, newReview.rate, newReview.text)
        await this.fetchMyReviews()
      } catch (e) {
        console.error('addReview error:', e)
      }
    },

    async updateReview(updatedReview) {
      try {
        await updateReview(this.userId, updatedReview.book_id, updatedReview.rate, updatedReview.text)
        await this.fetchMyReviews()
      } catch (e) {
        console.error('updateReview error:', e)
      }
    },

    async deleteReview(review) {
      try {
        await deleteReview(this.userId, review.book_id)
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
