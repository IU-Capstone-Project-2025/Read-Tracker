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

const booksStore = useBooksStore()
const reviewsStore = useReviewsStore()

onMounted(async () => {
  await reviewsStore.fetchMyReviews()
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
  height: 200px;
  position: relative;
}

.review-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.book-cover-container {
  width: 150px;
  height: 100%;
  flex-shrink: 0;
  position: relative;
}

.book-cover {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.review-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  max-height: 100%;
  box-sizing: border-box;
}

.book-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
}

.book-author {
  color: #667eea;
  font-size: 14px;
  margin-bottom: 10px;
  font-style: italic;
}

.review-text {
  color: #444;
  font-size: 14px;
  line-height: 1.5;
  margin-top: 5px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  line-clamp: 3;
  text-overflow: ellipsis;
  flex-grow: 1;
}

@media (max-width: 768px) {
  .review-card {
    flex-direction: column;
    height: auto;
    max-height: 400px;
  }
  
  .book-cover-container {
    width: 100%;
    height: 200px;
  }
  
  .review-content {
    padding: 15px;
    overflow-y: visible;
  }

  .review-text {
    -webkit-line-clamp: 6;
    line-clamp: 6;
  }
}
</style>