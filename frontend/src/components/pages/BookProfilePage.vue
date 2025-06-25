<template>
  <div v-if="loading" class="book-profile">
    <p>Loading book data...</p>
  </div>

  <div v-else class="book-profile">
    <div class="book-header">
      <div class="cover-container">
        <img :src="book.cover" :alt="book.title" class="book-cover">
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
        <NoteForm :book-id="book.id" @note-saved="addNote" />
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
const bookId = route.params.id // UUID

const notesStore = useNotesStore()
const reviewsStore = useReviewsStore()

const book = ref(null)
const editingReview = ref(false)
const loading = ref(true)

onMounted(async () => {
  const loadedBooks = await fetchBooks()
  const found = loadedBooks.find(b => b.id === bookId)

  book.value = found || {
    id: bookId,
    title: `Book ${bookId}`,
    author: 'Unknown Author',
    genre: 'Unknown Genre',
    description: 'Book description not available.',
    cover: '/path/to/default-cover.jpg'
  }

  loading.value = false
})

const notes = computed(() => notesStore.getNotesForBook(bookId))
const existingReview = computed(() => reviewsStore.getReviewForBook(bookId))

watch(() => route.query, (query) => {
  if (query.editReview) {
    editingReview.value = true
  }
})

const addNote = (newNote) => {
  notesStore.addNote({ ...newNote, bookId })
}

const deleteNote = (noteId) => {
  notesStore.deleteNote(noteId)
}

const saveReview = (reviewData) => {
  if (editingReview.value) {
    reviewsStore.updateReview({
      ...existingReview.value,
      ...reviewData
    })
  } else {
    reviewsStore.addReview({ 
      ...reviewData, 
      bookId,
      createdAt: new Date().toISOString()
    })
  }
  editingReview.value = false
}

const startEditReview = () => {
  editingReview.value = true
}

const cancelEdit = () => {
  editingReview.value = false
}

const deleteReview = () => {
  reviewsStore.deleteReview(existingReview.value.id)
  editingReview.value = false
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
  width: 100%;
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