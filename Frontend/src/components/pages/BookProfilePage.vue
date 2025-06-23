<template>
  <div class="book-profile">
    <div class="book-header">
      <div class="book-cover-container">
        <img :src="book.cover" :alt="book.title" class="book-cover">
      </div>
      <div class="book-info">
        <h1 class="book-title">{{ book.title }}</h1>
        <p class="book-author">by {{ book.author }}</p>
        <p class="book-genre">{{ book.genre }}</p>
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
          v-if="!existingReview"
          :book-id="book.id"
          @review-saved="addReview"
        />
        <ReviewDisplay 
          v-else
          :review="existingReview" 
          @edit-review="handleEditReview"
          @delete-review="deleteReview"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NoteForm from '@/components/notes/NoteForm.vue'
import NoteList from '@/components/notes/NoteList.vue'
import ReviewEditor from '@/components/reviews/ReviewEditor.vue'
import ReviewDisplay from '@/components/reviews/ReviewDisplay.vue'
import { useNotesStore } from '@/store/notes'
import { useReviewsStore } from '@/store/reviews'

const route = useRoute()
const bookId = parseInt(route.params.id)
const notesStore = useNotesStore()
const reviewsStore = useReviewsStore()

// Sample book data - in a real app, this would come from an API
const book = ref({
  id: bookId,
  title: 'Sample Book Title',
  author: 'Author Name',
  genre: 'Fiction',
  description: 'This is a sample book description. It provides an overview of the book content and themes.',
  cover: '/path/to/cover.jpg'
})

const notes = computed(() => notesStore.getNotesForBook(bookId))
const existingReview = computed(() => reviewsStore.getReviewForBook(bookId))

const addNote = (newNote) => {
  notesStore.addNote({ ...newNote, bookId })
}

const deleteNote = (noteId) => {
  notesStore.deleteNote(noteId)
}

const addReview = (newReview) => {
  reviewsStore.addReview({ ...newReview, bookId })
}

const handleEditReview = () => {
  reviewsStore.setEditingReview(existingReview.value.id)
}

const deleteReview = () => {
  reviewsStore.deleteReview(existingReview.value.id)
}

onMounted(() => {
  // In a real app, you would fetch book details from an API here
  console.log(`Loading book details for ID: ${bookId}`)
})
</script>

<style scoped>
.book-profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.book-header {
  display: flex;
  gap: 40px;
  margin-bottom: 40px;
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

.book-cover-container {
  flex: 0 0 300px;
}

.book-cover {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.book-info {
  flex: 1;
}

.book-title {
  font-size: 32px;
  color: #764ba2;
  margin-bottom: 10px;
}

.book-author {
  font-size: 22px;
  color: #667eea;
  margin-bottom: 15px;
}

.book-genre {
  font-size: 18px;
  color: #666;
  margin-bottom: 20px;
  font-style: italic;
}

.book-description {
  font-size: 16px;
  line-height: 1.6;
  color: #444;
}

.content-sections {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.notes-section,
.reviews-section {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
}

h2 {
  color: #764ba2;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(118, 75, 162, 0.1);
}

@media (max-width: 900px) {
  .book-header {
    flex-direction: column;
  }
  
  .content-sections {
    grid-template-columns: 1fr;
  }
  
  .book-cover-container {
    flex: none;
    max-width: 250px;
    margin: 0 auto;
  }
}
</style>