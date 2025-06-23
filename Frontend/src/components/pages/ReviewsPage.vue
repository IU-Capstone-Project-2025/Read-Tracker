<template>
  <div class="profile-container">
    <div class="page-header">
      <h1 class="page-title">My Reviews</h1>
      <p class="page-subtitle">Your thoughts on the books you've read</p>
    </div>

    <div class="reviews-grid">
      <div 
        class="review-card" 
        v-for="review in userReviews" 
        :key="review.id"
        @click="goToBookProfile(review.bookId)"
      >
        <div class="book-cover-container">
          <img class="book-cover" :src="review.cover" :alt="review.title" />
        </div>
        <div class="review-details">
          <div class="review-header">
            <h3 class="book-title">{{ review.title }}</h3>
            <div class="visibility-tag" :class="{ 'public': review.isPublic, 'private': !review.isPublic }">
              {{ review.isPublic ? 'Public' : 'Private' }}
            </div>
          </div>
          <span class="book-author">{{ review.author }}</span>
          <div class="review-rating">{{ review.rating }}/10</div>
          <p class="review-text">"{{ review.content }}"</p>
          <div class="review-date">{{ formatDate(review.createdAt) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewsStore } from '@/store/reviews'

const router = useRouter()
const reviewsStore = useReviewsStore()
const userReviews = ref([])

onMounted(() => {
  userReviews.value = reviewsStore.getAllReviews()
})

const goToBookProfile = (bookId) => {
  router.push({ name: 'bookProfile', params: { id: bookId } })
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
.reviews-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
  gap: 30px;
}

.review-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
  display: flex;
  height: 100%;
  cursor: pointer;
}

.review-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.book-cover-container {
  flex: 0 0 150px;
  height: 220px;
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.review-details {
  flex: 1;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.book-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-right: 15px;
}

.visibility-tag {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: 500;
  flex-shrink: 0;
}

.public {
  background-color: rgba(46, 204, 113, 0.2);
  color: #27ae60;
}

.private {
  background-color: rgba(52, 152, 219, 0.2);
  color: #2980b9;
}

.book-author {
  color: #667eea;
  font-size: 15px;
  margin-bottom: 12px;
  display: block;
}

.review-rating {
  font-size: 18px;
  font-weight: bold;
  color: #764ba2;
  margin-bottom: 12px;
}

.review-text {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 15px;
  flex: 1;
  font-style: italic;
}

.review-date {
  font-size: 12px;
  color: #999;
  text-align: right;
}

@media (max-width: 768px) {
  .reviews-grid {
    grid-template-columns: 1fr;
  }
  
  .review-card {
    flex-direction: column;
    height: auto;
  }
  
  .book-cover-container {
    flex: none;
    height: 200px;
  }
}
</style>