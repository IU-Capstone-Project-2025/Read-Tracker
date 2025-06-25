import axios from 'axios'

export async function saveNoteApi(noteData) {
  const response = await axios.post('http://localhost:8000/notes/', noteData)
  if (!response.data || !response.data.data || !response.data.data.length) {
    throw new Error('Invalid response from server')
  }
  return response.data.data[0]
}
