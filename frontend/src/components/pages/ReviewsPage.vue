<template>
  <div class="reviews-page">
    <div class="page-header">
      <h1 class="page-title">My Reviews</h1>
      <p class="page-subtitle">Your thoughts on the books you've read</p>
    </div>

    <div class="reviews-grid">
      <div 
        class="review-card" 
        v-for="review in userReviews" 
        :key="review.id"
      >
        <div class="card-top" @click="goToBookProfile(review.bookId)">
          <div class="review-content">
            <div class="review-header">
              <h3 class="book-title">{{ getBookTitle(review.bookId) }}</h3>
              <div class="review-meta">
                <div class="review-rating">{{ review.rating }}/10</div>
                <div class="visibility-tag" :class="{ 'public': review.isPublic, 'private': !review.isPublic }">
                  {{ review.isPublic ? 'Public' : 'Private' }}
                </div>
              </div>
            </div>
            <p class="review-text">{{ review.content }}</p>
          </div>
        </div>
        
        <div class="review-footer">
          <div class="review-date">{{ formatDate(review.createdAt) }}</div>
          <div class="review-actions">
            <button @click="editReview(review)" class="edit-btn">Edit</button>
            <button @click="deleteReview(review)" class="delete-btn">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewsStore } from '@/store/reviews'
import { useBooksStore } from '@/store/books'
import { fetchBooks } from '@/api/books'

const router = useRouter()
const reviewsStore = useReviewsStore()
const booksStore = useBooksStore()

const userReviews = ref([])
const books = computed(() => booksStore.books)

const getBookTitle = (bookId) => {
  const book = books.value.find(b => b.id === bookId)
  return book ? book.title : `Book ${bookId}`
}

onMounted(async () => {
  if (!booksStore.books.length) {
    const booksData = await fetchBooks()
    booksStore.initializeBooks(booksData)
  }
  userReviews.value = reviewsStore.getAllReviews()
})

const goToBookProfile = (bookId) => {
  router.push({ name: 'bookProfile', params: { id: bookId } })
}

const editReview = (review) => {
  router.push({ 
    name: 'bookProfile', 
    params: { id: review.bookId },
    query: { editReview: review.id }
  })
}

const deleteReview = (review) => {
  if (confirm('Are you sure you want to delete this review?')) {
    reviewsStore.deleteReview(review.id)
    userReviews.value = reviewsStore.getAllReviews()
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}
</script>

<style scoped>
.reviews-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.reviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 20px;
}

.review-card {
  background: white;
  border-radius: 10px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.card-top {
  cursor: pointer;
  margin-bottom: 15px;
}

.review-content {
  display: flex;
  flex-direction: column;
}

.review-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  align-items: center;
}

.book-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-right: 10px;
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.review-rating {
  font-weight: bold;
  color: #764ba2;
  font-size: 16px;
}

.visibility-tag {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: 500;
}

.public {
  background-color: rgba(46, 204, 113, 0.2);
  color: #27ae60;
}

.private {
  background-color: rgba(52, 152, 219, 0.2);
  color: #2980b9;
}

.review-text {
  color: #555;
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 5px;
}

.review-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #eee;
  margin-top: auto;
}

.review-date {
  font-size: 13px;
  color: #777;
}

.review-actions {
  display: flex;
  gap: 10px;
}

.edit-btn, .delete-btn {
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid;
}

.edit-btn {
  background: none;
  border-color: #764ba2;
  color: #764ba2;
}

.edit-btn:hover {
  background: #764ba2;
  color: white;
}

.delete-btn {
  background: none;
  border-color: #e74c3c;
  color: #e74c3c;
}

.delete-btn:hover {
  background: #e74c3c;
  color: white;
}

@media (max-width: 768px) {
  .reviews-grid {
    grid-template-columns: 1fr;
  }
  
  .review-card {
    padding: 15px;
  }
  
  .review-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>
