<template>
  <div class="note-list">
    <div v-if="notes.length === 0" class="empty-notes">
      No notes yet. Add your first note!
    </div>
    
    <div v-else>
      <NoteItem 
        v-for="note in notes" 
        :key="note.id" 
        :note="note"
        @delete="deleteNote"
      />
    </div>
  </div>
</template>

<script setup>
import NoteItem from './NoteItem.vue'

const props = defineProps({
  notes: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['delete-note'])

const deleteNote = (noteId) => {
  emit('delete-note', noteId)
}
</script>

<style scoped>
.empty-notes {
  text-align: center;
  color: #888;
  padding: 20px;
  font-style: italic;
}
</style>