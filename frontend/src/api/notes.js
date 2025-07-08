import axios from 'axios'
import config from '@/runtimeConfig'

const api = axios.create({
  baseURL: config.api.baseUrl
})


export const getNotes = async (userId, bookId) => {
  try {
    console.log(`[API] Fetching notes for book ID: ${bookId}`)
    const response = await api.post(`me/books/${bookId}/notes`, {
      user_id: userId
    })
    
    if (response.status !== 'success') {
      const errorMsg = response.message || 'Failed to load notes. Please try again.'
      console.error('[API] fetchBookNotes error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Successfully fetched ${response.data.length} notes for book ID: ${bookId}`)
    return response.data
  } catch (error) {
    const errorMsg = error.response?.message || 
                    'Failed to load notes. Please check your connection and try again.'
    console.error('[API] fetchBookNotes exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const createNote = async (userId, bookId, text) => {
  try {
    console.log(`[API] Creating note for book ID: ${bookId}`)
    const response = await api.put(`/me/books/${bookId}/notes`, {
      user_id: userId,
      text: text.text
    })
    
    if (response.status !== 'success') {
      const errorMsg = response.message || 'Failed to create your note. Please try again.'
      console.error('[API] saveNoteApi error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Note created successfully for book ID: ${bookId}`)
    return response.data
  } catch (error) {
    const errorMsg = error.response?.message || 
                    'Failed to create note. Please check your connection and try again.'
    console.error('[API] saveNoteApi exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const deleteNote = async (userId, noteId) => {
  try {
    console.log(`[API] Deleting note ID: ${noteId}`)
    const response = await api.delete(`me/notes/${noteId}`, {
      data: {
        user_id: userId
      }
    })
    
    if (response.status !== 'success') {
      const errorMsg = response.message || 'Failed to delete note. Please try again.'
      console.error('[API] deleteNoteApi error:', errorMsg)
      throw new Error(errorMsg)
    }

    console.log(`[API] Note deleted successfully: ${noteId}`)
    return response.data
  } catch (error) {
    const errorMsg = error.response?.message || 
                    'Failed to delete note. Please check your connection and try again.'
    console.error('[API] deleteNoteApi exception:', errorMsg, error)
    throw new Error(errorMsg)
  }
}

export const updateNote = async (userId, noteId, text) => {
  try {
    const response = await api.put(`me/notes/${noteId}`, {
      user_id: userId,
      text: text.text
    })
    return response.data
  } catch (error) {
    console.error(`Failed to update note:`, error)
    throw error
  }
}