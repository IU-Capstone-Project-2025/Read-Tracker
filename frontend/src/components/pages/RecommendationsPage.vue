<template>
  <div class="page-content">
    <div class="page-header">
      <h1 class="page-title">Book Recommendations</h1>
      <p class="page-subtitle">Based on your subscriptions</p>
    </div>

    <div class="recommendations-feed">
      <div 
        class="review-card" 
        v-for="(review, index) in reviewsWithBooks" 
        :key="index"
      >
        <div class="book-cover-container">
          <img 
            v-if="review.book.cover" 
            :src="review.book.cover" 
            :alt="review.book.title" 
            class="book-cover"
          />
          <img 
            v-else 
            src="/images/placeholder.png" 
            alt="No cover available" 
            class="book-cover"
          />
        </div>
        
        <div class="review-content">
          <h3 class="book-title">{{ review.book.title }}</h3>
          <p class="book-author">{{ review.book.author }}</p>
          <div class="review-text">
            <p>{{ review.text }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useBooksStore } from '@/store/books'
import { useReviewsStore } from '@/store/reviews'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()
const booksStore = useBooksStore()
const reviewsStore = useReviewsStore()
const loading = ref(true)

onMounted(async () => {
  try {
    loading.value = true

    // Only fetch if not already initialized
    if (!reviewsStore.reviews.length) {
      await reviewsStore.fetchMyReviews()
    }
  } catch (error) {
    console.error('Failed to load recommendations:', error)
  } finally {
    loading.value = false
  }
})

const reviewsWithBooks = computed(() => {
  return reviewsStore.reviews.map(review => {
    const book = booksStore.books.find(b => b.id === review.book_id) || {}
    return {
      ...review,
      book: {
        id: book.id || review.book_id,
        title: book.title || 'Unknown Book',
        author: book.author || 'Unknown Author',
        cover: book.cover || ''
      }
    }
  })
})
</script>

<style scoped>
.page-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-size: 32px;
  color: #764ba2;
  font-weight: 600;
  margin-bottom: 8px;
}

.page-subtitle {
  color: #666;
  font-size: 18px;
}

.recommendations-feed {
  display: flex;
  flex-direction: column;
  gap: 30px;
  max-width: 800px;
  margin: 0 auto;
}

.review-card {
  display: flex;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.review-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.book-cover-container {
  width: 150px;
  height: 200px;
  flex-shrink: 0;
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.review-content {
  padding: 25px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.book-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.book-author {
  color: #667eea;
  font-size: 16px;
  margin-bottom: 15px;
  font-style: italic;
}

.review-text {
  color: #444;
  font-size: 16px;
  line-height: 1.6;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .review-card {
    flex-direction: column;
  }

  .book-cover-container {
    width: 100%;
    height: 250px;
  }

  .review-content {
    padding: 20px;
  }
}
</style>
