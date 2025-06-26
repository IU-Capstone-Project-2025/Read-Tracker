import axios from 'axios'
import { defineStore } from 'pinia'

export const useNotesStore = defineStore('notes', {
  state: () => ({
    notes: JSON.parse(localStorage.getItem('bookNotes')) || []
  }),
  
  actions: {
    async fetchNotes(bookId) {
      const response = await axios.get(`http://localhost:8000/me/books/${bookId}/notes`)
      if (response.data.status !== 'success') throw new Error('Failed to fetch notes')
      
      this.notes = response.data.data
      this.persistNotes()
    },
    
    async addNote(bookId, noteData) {
      const postResponse = await axios.post(`http://localhost:8000/me/books/${bookId}/notes`, noteData)
      if (postResponse.data.status !== 'success') throw new Error('Failed to add note')

      await this.fetchNotes(bookId)
    },
    
    deleteNote(noteId) {
      this.notes = this.notes.filter(note => note.id !== noteId)
      this.persistNotes()
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
