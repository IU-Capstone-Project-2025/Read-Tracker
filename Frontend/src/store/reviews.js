import { defineStore } from 'pinia'

export const useReviewsStore = defineStore('reviews', {
  state: () => ({
    reviews: JSON.parse(localStorage.getItem('bookReviews')) || [],
    editingReviewId: null
  }),
  
  actions: {
    addReview(newReview) {
      this.reviews = this.reviews.filter(r => r.bookId !== newReview.bookId)
      this.reviews.push(newReview)
      this.persistReviews()
    },
    
    updateReview(updatedReview) {
      const index = this.reviews.findIndex(r => r.id === updatedReview.id)
      if (index !== -1) {
        this.reviews[index] = updatedReview
        this.persistReviews()
      }
    },
    
    deleteReview(reviewId) {
      this.reviews = this.reviews.filter(r => r.id !== reviewId)
      this.persistReviews()
    },
    
    setEditingReview(reviewId) {
      this.editingReviewId = reviewId
    },
    
    persistReviews() {
      localStorage.setItem('bookReviews', JSON.stringify(this.reviews))
    },
    
    getAllReviews() {
      return this.reviews.map(review => ({
        ...review,
        title: `Book ${review.bookId}`,
        author: 'Author Name',
        cover: '/path/to/default-cover.jpg'
      }))
    }
  },
  
  getters: {
    getReviewForBook: (state) => (bookId) => {
      return state.reviews.find(review => review.bookId === bookId)
    }
  }
})