<template>
  <div class="profile-container">
    <div class="page-header">
      <h1 class="page-title">My Collections</h1>
      <p class="page-subtitle">Organize your books into collections</p>
    </div>

    <button class="reviews-button" style="margin-bottom: 20px;">
      <i class="fas fa-plus"></i> Create New Collection
    </button>

    <div class="collections-grid">
      <div class="collection-card" v-for="collection in collections" :key="collection.title">
        <div class="collection-header">
          <h3 class="collection-title">{{ collection.title }}</h3>
          <div class="book-count">{{ collection.books.length }} books</div>
        </div>
        <div class="collection-books">
          <div class="collection-book" v-for="book in collection.books" :key="book.title">
            <img class="collection-book-cover" :src="book.cover" />
            <div>
              <div class="collection-book-title">{{ book.title }}</div>
              <div class="book-author">{{ book.author }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const collections = ref([
  {
    title: 'Science Fiction',
    books: [
      {
        title: 'Project Hail Mary',
        author: 'Andy Weir',
        cover: 'https://m.media-amazon.com/images/I/91Bc+UJQn0L._AC_UF1000,1000_QL80_.jpg'
      },
      {
        title: 'Dune',
        author: 'Frank Herbert',
        cover: 'https://m.media-amazon.com/images/I/81tz8z0CjQL._AC_UF1000,1000_QL80_.jpg'
      },
      {
        title: 'The Three-Body Problem',
        author: 'Liu Cixin',
        cover: 'https://m.media-amazon.com/images/I/81u5sZR7tmL._AC_UF1000,1000_QL80_.jpg'
      }
    ]
  },
  {
    title: 'Personal Development',
    books: [
      {
        title: 'Atomic Habits',
        author: 'James Clear',
        cover: 'https://m.media-amazon.com/images/I/91uwocAMtSL._AC_UF1000,1000_QL80_.jpg'
      },
      {
        title: 'Deep Work',
        author: 'Cal Newport',
        cover: 'https://m.media-amazon.com/images/I/71eJk7GtUOL._AC_UF1000,1000_QL80_.jpg'
      },
      {
        title: 'The Power of Now',
        author: 'Eckhart Tolle',
        cover: 'https://m.media-amazon.com/images/I/81bsw6fnUiL._AC_UF1000,1000_QL80_.jpg'
      }
    ]
  },
  {
    title: 'Classic Literature',
    books: [
      {
        title: 'Pride and Prejudice',
        author: 'Jane Austen',
        cover: 'https://m.media-amazon.com/images/I/71MvRl2gB0L._AC_UF1000,1000_QL80_.jpg'
      },
      {
        title: 'To Kill a Mockingbird',
        author: 'Harper Lee',
        cover: 'https://m.media-amazon.com/images/I/81MlNaXc3fL._AC_UF1000,1000_QL80_.jpg'
      },
      {
        title: '1984',
        author: 'George Orwell',
        cover: 'https://m.media-amazon.com/images/I/71tRf2Y5SwL._AC_UF1000,1000_QL80_.jpg'
      }
    ]
  }
])
</script>
