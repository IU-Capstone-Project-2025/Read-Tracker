import { defineStore } from 'pinia'
import { useAuthStore } from '@/store/auth'
import {
  apiFetchBooks,
  apiFetchBook,
  apiCreateBook,
  apiFetchUserBooks,
  apiAddUserBook
} from '@/api/books'

export const useBooksStore = defineStore('books', {
  state: () => ({
    userId: null,
    allBooks: [],
    userBooks: JSON.parse(localStorage.getItem('userBooks')) || []
  }),

  actions: {
    async init(userId) {
      this.userId = userId
    },
    async fetchAllBooks() {
      try {
        const booksData = await apiFetchBooks();
        this.allBooks = booksData;
        this.persistBooks()
        return booksData
      } catch (error) {
        console.error('Failed to fetch all books:', error);
      }
    },
    async fetchUserBooks(userId) {
      const userBooksData = await apiFetchUserBooks(userId);
      this.userBooks = userBooksData.map(ub => ({
        bookId: ub.book_id,
        status: ub.status,
        startDate: ub.start_date,
        endDate: ub.end_date,
        }));
      this.persistBooks()
      return userBooksData
      },

    async fetchBook(bookId) {
      const bookData = await apiFetchBook(bookId)
      return bookData
    },

    async addBookToUserCollection(bookId) {
      const authStore = useAuthStore()
      if (!authStore.user || !authStore.user.id) {
        throw new Error('User not authenticated')
      }
      if (this.userBooks.some(book => book.bookId === bookId)) {
        throw new Error('Book is already in your collection')
      }
      try {
        const status = 'want to read'
        const userBook = await apiAddUserBook(authStore.user.id, bookId, status)
        console.log('Status: ${userBook.status}')
        await this.fetchUserBooks(this.userId)
      } catch (error) {
        throw error
      }
    },

    async updateUserBookStatus(bookId, newStatus) {
      const userBook = this.userBooks.find(ub => ub.bookId === bookId);
      if (userBook) {
        userBook.status = newStatus;
        this.persistBooks()
      }
    },
    
    async persistBooks() {
      localStorage.setItem('userBooks', JSON.stringify(this.userBooks))
    }
  },
  getters: {
    userBooksWithDetails(state) {
      return state.userBooks.map(ub => {
        const book = state.allBooks.find(b => b.id === ub.bookId);
        if (!book) {
          console.warn(`Book with id ${ub.bookId} not found in allBooks`);
          return null;
        }
        const mergedBook = { ...book, ...ub, id: ub.bookId };
        console.log('[Store] Merged book cover:', {
          id: mergedBook.id,
          title: mergedBook.title,
          cover: mergedBook.cover
        });
        return mergedBook;
      }).filter(book => book !== null);
    },
  },
});