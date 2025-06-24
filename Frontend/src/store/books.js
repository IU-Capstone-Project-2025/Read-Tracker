import { defineStore } from 'pinia'

export const useBooksStore = defineStore('books', {
  state: () => ({
    books: JSON.parse(localStorage.getItem('userBooks')) || []
  }),
  
  actions: {
    initializeBooks(booksData) {
      this.books = booksData.map(book => ({
        ...book,
        status: 'to-read',
        addedDate: Date.now()
      }))
      this.persistBooks()
    },
    
    updateBookStatus(bookId, newStatus) {
      const book = this.books.find(b => b.id === bookId)
      if (book) {
        book.status = newStatus
        this.persistBooks()
      }
    },
    
    persistBooks() {
      localStorage.setItem('userBooks', JSON.stringify(this.books))
    }
  }
})