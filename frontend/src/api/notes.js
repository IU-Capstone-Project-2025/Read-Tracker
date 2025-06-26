import axios from 'axios'

export async function saveNoteApi(bookID, noteData) {
  const postResponse = await axios.post(`http://localhost:8000/me/books/${bookID}/notes`, noteData)

  if (postResponse.data.status !== 'success') {
    throw new Error('Failed to add note')
  }

  const getResponse = await axios.get(`http://localhost:8000/me/books/${bookID}/notes`)

  if (getResponse.data.status !== 'success') {
    throw new Error('Failed to fetch notes')
  }

  return getResponse.data.data
}