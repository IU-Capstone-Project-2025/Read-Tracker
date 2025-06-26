<template>
  <div v-if="loading" class="book-profile">
    <p>Loading book data...</p>
  </div>

  <div v-else class="book-profile">
    <div class="book-header">
      <div class="cover-container">
        <img 
          v-if="book.cover" 
          :src="book.cover" 
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
        <p class="book-meta">{{ book.genre }} • Published 2023</p>
        <p class="book-description">{{ book.description }}</p>
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
import NoteForm from '@/components/notes/NoteForm.vue'
import NoteList from '@/components/notes/NoteList.vue'
import ReviewEditor from '@/components/reviews/ReviewEditor.vue'
import ReviewDisplay from '@/components/reviews/ReviewDisplay.vue'
import { useNotesStore } from '@/store/notes'
import { useReviewsStore } from '@/store/reviews'
import { fetchBooks } from '@/api/books'

const route = useRoute()
const bookId = route.params.id

const notesStore = useNotesStore()
const reviewsStore = useReviewsStore()

const book = ref(null)
const loading = ref(true)
const editingReview = ref(false)

onMounted(async () => {
  try {
    const loadedBooks = await fetchBooks()
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
  } catch (e) {
    console.error('Failed to load book, notes or reviews:', e)
  } finally {
    loading.value = false
  }
})

const notes = computed(() => notesStore.getNotesForBook(bookId))
const existingReview = computed(() => reviewsStore.getReviewForBook(bookId))

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
    await notesStore.deleteNote(noteId)
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
    console.log('Reviews from store:', reviewsStore.reviews)
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

.content-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
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
