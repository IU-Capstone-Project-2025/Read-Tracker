<template>
  <div class="page-content">
    <div class="page-header">
      <h1 class="page-title">Book Recommendations</h1>
      <p class="page-subtitle">Based on your subscriptions</p>
    </div>

    <div class="recommendations-feed">
      <div 
        class="review-card"
        @click="goToBook(review.book.id)"
        v-for="(review, index) in reviewsWithBooks" 
        :key="index"
      >
        <div class="book-cover-container">
          <img 
            v-if="review.book.cover" 
            :src="`/images/${review.book.cover}.jpg`"
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
          <div class="review-header">
            <div class="book-info">
              <h3 class="book-title">{{ review.book.title }}</h3>
              <p class="book-author">{{ review.book.author }}</p>
            </div>
            <div class="user-profile">
              <img 
                src="/images/placeholder.png" 
                alt="No avatar available" 
                class="avatar"
              />
              <span class="username">{{ review.username }}</span>
            </div>
          </div>

          <div class="review-text" :class="{ expanded: isExpanded(index) }">
            <p v-if="isExpanded(index)">
              {{ review.text }}
            </p>
            <p v-else>
              {{ truncate(review.text, 150) }}
            </p>
          </div>

          <button 
            v-if="showToggleButton(review.text)" 
            class="expand-button" 
            @click.stop="toggleExpand(index)"
          >
            {{ isExpanded(index) ? 'Hide' : 'Expand' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useBooksStore } from '@/store/books'
import { useSubscriptionsStore } from '@/store/subscriptions'
import { useUsersStore } from '@/store/users'

const router = useRouter()
const booksStore = useBooksStore()
const reviewsStore = useSubscriptionsStore()
const usersStore = useUsersStore()
const usernames = ref({})

onMounted(async () => {
  await reviewsStore.getAllReviews()
  for (const review of reviewsStore.reviews) {
    const userId = review.user_id
    if (!usernames.value[userId]) {
      const name = await fetchUsername(userId)
      usernames.value[userId] = name
    }
  }
})

const reviewsWithBooks = computed(() => {
  return reviewsStore.reviews.map(review => {
    const book = booksStore.allBooks.find(b => b.id === review.book_id) || {}
    return {
      ...review,
      book: {
        id: book.id || review.book_id,
        title: book.title || 'Unknown Book',
        author: book.author || 'Unknown Author',
        cover: book.cover || ''
      },
      username: usernames.value[review.user_id] || 'Loading...'
    }
  })
})

const goToBook = (bookId) => {
  router.push({ name: 'bookProfile', params: { id: bookId } })
}

const expandedReviews = ref([])

const isExpanded = (index) => expandedReviews.value.includes(index)

const toggleExpand = (index) => {
  if (isExpanded(index)) {
    expandedReviews.value = expandedReviews.value.filter(i => i !== index)
  } else {
    expandedReviews.value.push(index)
  }
}

const truncate = (text, limit) => {
  return text.length > limit ? text.slice(0, limit) + '...' : text
}

const showToggleButton = (text) => {
  return text.length > 150
}

const fetchUsername = async (userId) => {
  const userProfile = await usersStore.fetchUserProfile(userId)
  return userProfile?.username
}
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
  overflow: clip;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
  height: auto; 
  flex-direction: row;
  cursor: pointer;
}

.review-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.book-cover-container {
  width: 140px;
  height: 200px;
  flex-shrink: 0;
  margin: 0; 
  padding: 0;
  line-height: 0;
}

.book-cover {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  margin: 0;
}

.review-content {
  padding: 20px;
  flex: 1;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 12px;
}

.book-info {
  display: flex;
  flex-direction: column;
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
  margin-bottom: 0;
  font-style: italic;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-size: 16px;
  color: #333;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.review-text {
  color: #444;
  font-size: 14px;
  line-height: 1.5;
  margin-top: 10px;
  flex-grow: 1;
  overflow: hidden;
  max-height: 4.5em; 
  transition: max-height 0.3s ease, padding 0.3s ease;
  word-wrap: break-word; 
  white-space: normal;
  word-break: break-word;
  overflow-wrap: anywhere;
}

.review-text.expanded {
  max-height: none;
  overflow: visible;
  padding-bottom: 5px;
}

.expand-button {
  margin-top: 10px;
  padding: 8px 12px;
  background-color: #764ba2;
  border-radius: 40px;
  color: white;
  border: none;
  cursor: pointer;
  align-self: flex-start;
}

.expand-button:hover {
  background-color: #667eea;
  transform: translateY(-2px);
}
</style>
