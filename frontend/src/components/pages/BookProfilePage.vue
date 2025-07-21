<template>
  <div v-if="loading" class="book-profile">
    <p>Loading book data...</p>
  </div>

  <div v-else class="book-profile">
    <div class="book-header">
      <div class="cover-container">
        <img 
          v-if="book.cover" 
          :src="`/images/${book.cover}.jpg`"
          :alt="book.title" 
          class="book-cover"
        />
        <img 
          v-else 
          src="/images/placeholder.png" 
          alt="No cover available" 
          class="book-cover"
        />
      </div>
      <div class="book-info">
        <h1 class="book-title">{{ book.title }}</h1>
        <p class="book-author">by {{ book.author }}</p>
        <p class="book-description">{{ book.description }}</p>
      </div>
    </div>

    <!-- Community Reviews Section -->
    <div class="community-reviews-section">
      <h2>Community Reviews</h2>
      <div v-if="communityReviewsLoading" class="loading">Loading community reviews...</div>
      <div v-else>
        <div v-if="communityReviews.length" class="reviews-feed">
          <CommunityReviewCard 
            v-for="review in communityReviews" 
            :key="review.id" 
            :review="review" 
          />
        </div>
        <p v-else class="no-reviews">No community reviews yet. Be the first to review!</p>
      </div>
    </div>

    <div class="content-sections">
      <div class="notes-section">
        <h2>Your Notes</h2>
        <NoteForm :book-id="book.id" @note-saved="refreshNotes" />
        <NoteList :notes="notes" @delete-note="deleteNote" />
      </div>

      <div class="reviews-section">
        <h2>Your Review</h2>
        <ReviewEditor 
          v-if="!existingReview || editingReview"
          :book-id="book.id"
          :existing-review="editingReview ? existingReview : null"
          @review-saved="saveReview"
          @cancel-edit="cancelEdit"
        />
        <ReviewDisplay 
          v-else
          :review="existingReview" 
          @edit-review="startEditReview"
          @delete-review="deleteReview"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/store/auth'
import NoteForm from '@/components/notes/NoteForm.vue'
import NoteList from '@/components/notes/NoteList.vue'
import ReviewEditor from '@/components/reviews/ReviewEditor.vue'
import ReviewDisplay from '@/components/reviews/ReviewDisplay.vue'
import CommunityReviewCard from '@/components/reviews/CommunityReviewCard.vue'
import { useNotesStore } from '@/store/notes'
import { useReviewsStore } from '@/store/reviews'
import { useBooksStore } from '@/store/books'
import { useSubscriptionsStore } from '@/store/subscriptions'
import { useUsersStore } from '@/store/users'

const route = useRoute()
const bookId = route.params.id

const authStore = useAuthStore()
const notesStore = useNotesStore()
const reviewsStore = useReviewsStore()
const booksStore = useBooksStore()
const subscriptionsStore = useSubscriptionsStore()
const usersStore = useUsersStore()

const book = ref(null)
const loading = ref(true)
const editingReview = ref(false)
const communityReviewsLoading = ref(true)

onMounted(async () => {
  try {
    const loadedBooks = await booksStore.fetchAllBooks()
    const found = loadedBooks.find(b => b.id === bookId)
    book.value = found || {
      id: bookId,
      title: `Book ${bookId}`,
      author: 'Unknown Author',
      genre: 'Unknown Genre',
      description: 'Book description not available.',
      cover: '/images/placeholder.png'
    }
    await notesStore.fetchNotes(bookId)
    await reviewsStore.fetchReviews(bookId)
    await reviewsStore.fetchCommunityReviews(bookId)
    
    if (authStore.isAuthenticated) {
      await subscriptionsStore.fetchSubscriptions(authStore.user_id)
    }
  } catch (e) {
    console.error('Failed to load book, notes or reviews:', e)
  } finally {
    loading.value = false
    communityReviewsLoading.value = false
  }
})

const notes = computed(() => notesStore.getNotesForBook(bookId))
const existingReview = computed(() => reviewsStore.getReviewForBook(bookId))
const communityReviews = computed(() => reviewsStore.communityReviews)

watch(() => route.query, (query) => {
  editingReview.value = !!query.editReview
})

const refreshNotes = async () => {
  try {
    await notesStore.fetchNotes(bookId)
  } catch (e) {
    console.error('Failed to refresh notes:', e)
  }
}

const deleteNote = async (noteId) => {
  try {
    await notesStore.deleteNote(bookId, noteId)
    await refreshNotes()
  } catch (e) {
    console.error('Failed to delete note:', e)
  }
}

const saveReview = async (reviewData) => {
  if (!bookId) {
    console.error('BookId is undefined!')
    return
  }
  try {
    if (editingReview.value && existingReview.value) {
      await reviewsStore.updateReview(bookId, reviewData)
    } else {
      await reviewsStore.addReview(bookId, reviewData)
    }
    editingReview.value = false
    await reviewsStore.fetchReviews(bookId)
  } catch (e) {
    console.error('Failed to save review:', e)
  }
}

const startEditReview = () => {
  editingReview.value = true
}

const cancelEdit = () => {
  editingReview.value = false
}

const deleteReview = async () => {
  if (existingReview.value) {
    try {
      await reviewsStore.deleteReview(bookId)
      editingReview.value = false
      await reviewsStore.fetchReviews(bookId)
    } catch (e) {
      console.error('Failed to delete review:', e)
    }
  }
}
</script>

<style scoped>
.book-profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.book-header {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

.cover-container {
  flex-shrink: 0;
  width: 200px;
  display: flex;
  align-items: flex-start;
}

.book-cover {
  position: relative;
  width: 100%;
  height: 100%;
  max-height: 300px;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.book-info {
  flex: 1;
  min-width: 0;
}

.book-title {
  font-size: 28px;
  color: #764ba2;
  margin-bottom: 8px;
}

.book-author {
  font-size: 18px;
  color: #667eea;
  margin-bottom: 5px;
}

.book-meta {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
}

.book-description {
  font-size: 15px;
  line-height: 1.6;
  color: #444;
}

.community-reviews-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
  margin-bottom: 20px;
}

.reviews-feed {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 10px;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.no-reviews {
  text-align: center;
  color: #888;
  font-style: italic;
  padding: 15px;
}

.content-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.notes-section,
.reviews-section {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.08);
}

h2 {
  font-size: 20px;
  color: #764ba2;
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(118, 75, 162, 0.1);
}

@media (max-width: 900px) {
  .book-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .content-sections {
    grid-template-columns: 1fr;
  }
  
  .cover-container {
    width: 150px;
    margin-bottom: 15px;
  }
}

@media (max-width: 600px) {
  .book-header {
    padding: 15px;
  }
  
  .book-title {
    font-size: 24px;
  }
  
  .book-author {
    font-size: 16px;
  }
}
</style>
