import axios from 'axios'
import { defineStore } from 'pinia'
import {
  getNotes,
  createNote,
  deleteNote,
  updateNote
} from '@/api/notes'


export const useNotesStore = defineStore('notes', {
  state: () => ({
    notes: [],
    userId: null
  }),
  
  actions: {
    async init(userId) {
      this.userId = userId
    },

    async fetchNotes(bookId) {
      try {
        const data = await getNotes(this.userId, bookId)
        this.notes = data.data
        this.persistNotes()
      }
      catch (e) {
        console.error('fetchNotes error:', e)
      }
    },
    
    async addNote(bookId, noteText) {
      try {
        await createNote(this.userId, bookId, noteText)
      await this.fetchNotes(bookId)
      }
      catch (e) {
        console.error('addNote error:', e)
      }
    },
    
    async updateNote(noteData, noteText) {
      try {
        await updateNote(this.userId, noteData.note_id, noteText)
        await this.fetchNotes(bookId)
      } catch (e) {
        console.error('updateReview error:', e)
      }
    },

    async deleteReview(noteData) {
      try {
        await deleteReview(this.userId, noteData.note_id)
        await this.fetchMyReviews()
      } catch (e) {
        console.error('deleteReview error:', e)
      }
    },
    
    persistNotes() {
      localStorage.setItem('bookNotes', JSON.stringify(this.notes))
    }
  },
  
  getters: {
    getNotesForBook: (state) => (bookId) => {
      return state.notes
        .filter(note => note.book_id === bookId)
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    }
  }
})
