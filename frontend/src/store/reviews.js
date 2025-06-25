import { defineStore } from 'pinia'
import { useBooksStore } from '@/store/books'

export const useReviewsStore = defineStore('reviews', {
  state: () => ({
    reviews: JSON.parse(localStorage.getItem('bookReviews')) || [],
    editingReviewId: null
  }),
  
  actions: {
    addReview(newReview) {
      const completeReview = {
        id: Date.now(),
        createdAt: new Date().toISOString(),
        ...newReview
      }
      this.reviews = this.reviews.filter(r => r.bookId !== newReview.bookId)
      this.reviews.push(completeReview)
      this.persistReviews()
      return completeReview
    },
    
    updateReview(updatedReview) {
      const index = this.reviews.findIndex(r => r.id === updatedReview.id)
      if (index !== -1) {
        this.reviews[index] = {
          ...this.reviews[index],
          ...updatedReview,
          updatedAt: new Date().toISOString()
        }
        this.persistReviews()
      }
    },
    
    deleteReview(reviewId) {
      this.reviews = this.reviews.filter(r => r.id !== reviewId)
      this.persistReviews()
    },
    
    persistReviews() {
      localStorage.setItem('bookReviews', JSON.stringify(this.reviews))
    },
    
    getAllReviews() {
      const booksStore = useBooksStore()
      return this.reviews.map(review => {
        const book = booksStore.books.find(b => b.id === review.bookId) || {}
        return {
          ...review,
          title: book.title || `Book ${review.bookId}`,
          author: book.author || 'Unknown Author',
          cover: book.cover || '/path/to/default-cover.jpg'
        }
      })
    },
    
    getReviewForBook(bookId) {
      return this.reviews.find(review => review.bookId === bookId)
    }
  }
})