import { defineStore } from 'pinia'
import { 
  fetchBooks,
  fetchBook,
  createBook
} from '@/api/books'

export const useBooksStore = defineStore('books', {
  state: () => ({
    userId: null,
    books: JSON.parse(localStorage.getItem('userBooks')) || []
  }),
  
  actions: {
    async init(userId) {
      this.userId = userId
    },
    
    async initializeBooks() {
      const booksData = await fetchBooks()
      this.books = booksData.map(book => ({
        ...book,
        status: 'to-read',
        addedDate: Date.now()
      }))
      this.persistBooks()
    },

    async fetchBooks(bookId) {
      try {
        const data = getNotes(this.userId, bookId)
        this.notes = data.data
        this.persistNotes()
      }
      catch (e) {
        console.error('fetchNotes error:', e)
      }
    },
    
    async updateBookStatus(bookId, newStatus) {
      const book = this.books.find(b => b.id === bookId)
      if (book) {
        book.status = newStatus
        this.persistBooks()
      }
    },
    
    async persistBooks() {
      localStorage.setItem('userBooks', JSON.stringify(this.books))
    }
  }
})