import { defineStore } from 'pinia'
import { 
  apiFetchBooks,
  apiFetchBook,
  apiCreateBook
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

    async fetchBook(bookId) {
      const bookData = await apiFetchBook(bookId)
      return bookData
    },
    
    async fetchBooks() {
      const booksData = await apiFetchBooks()
      this.books = booksData.map(book => ({
        ...book,
        status: 'to-read',
        addedDate: Date.now()
      }))
      this.persistBooks()
      return booksData
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