<template>
  <div class="note-form">
    <textarea v-model="noteContent" placeholder="Write your private notes here..." rows="4"></textarea>
    <button @click="saveNote" class="save-btn">Save Note</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  bookId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['note-saved'])

const noteContent = ref('')

const saveNote = () => {
  if (noteContent.value.trim()) {
    const newNote = {
      id: Date.now(),
      content: noteContent.value,
      createdAt: new Date().toISOString()
    }
    emit('note-saved', newNote)
    noteContent.value = ''
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

.save-btn:hover {
  background: #667eea;
}
</style>