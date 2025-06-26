<template>
  <div class="note-form">
    <textarea
      v-model="noteContent"
      placeholder="Write your private notes here..."
      rows="4"
      :disabled="loading"
    ></textarea>

    <button
      @click="saveNote"
      class="save-btn"
      :disabled="loading || !noteContent.trim()"
    >
      <span v-if="loading">Saving...</span>
      <span v-else>Save Note</span>
    </button>

    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useNotesStore } from '@/store/notes'

const props = defineProps({
  bookId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['note-saved'])

const noteContent = ref('')
const loading = ref(false)
const error = ref(null)

const notesStore = useNotesStore()

const saveNote = async () => {
  if (!noteContent.value.trim()) return

  loading.value = true
  error.value = null

  try {
    await notesStore.addNote(props.bookId, { text: noteContent.value })
    emit('note-saved')
    noteContent.value = ''
  } catch (err) {
    error.value = err.response?.data?.message || err.message || 'Error saving note'
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
.note-form {
  margin-bottom: 30px;
}

textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  margin-bottom: 12px;
  resize: vertical;
  min-height: 100px;
}

.save-btn {
  background: #764ba2;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.2s;
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.save-btn:hover:not(:disabled) {
  background: #667eea;
}

.error-message {
  color: #e53e3e;
  margin-top: 8px;
  font-weight: 500;
}
</style>
