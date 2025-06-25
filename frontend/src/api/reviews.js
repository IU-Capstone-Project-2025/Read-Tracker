import axios from 'axios'

export const getMyReviews = () => {
  return axios.get('http://localhost:8000/reviews/')
}

export const getBookReviews = (bookId) => {
  return axios.get(`http://localhost:8000/reviews/${bookId}`)
}

export const createReview = (bookId, review) => {
  return axios.post(`http://localhost:8000/me/reviews/${bookId}`, review)
}

export const updateReview = (bookId, review) => {
  return axios.put(`http://localhost:8000/me/reviews/${bookId}`, review)
}

export const deleteReview = (bookId) => {
  return axios.delete(`http://localhost:8000/me/reviews/${bookId}`)
}
