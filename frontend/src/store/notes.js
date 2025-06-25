import { defineStore } from 'pinia'

export const useNotesStore = defineStore('notes', {
  state: () => ({
    notes: JSON.parse(localStorage.getItem('bookNotes')) || []
  }),
  
  actions: {
    addNote(newNote) {
      this.notes.push(newNote)
      this.persistNotes()
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
        .filter(note => note.bookId === bookId)
        .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
    }
  }
})