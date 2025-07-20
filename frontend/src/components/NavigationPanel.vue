<template>
  <div class="sidebar" :class="{ collapsed: isCollapsed }">
    <div class="logo">
      <div class="logo-content">
        <span class="logo-icon"><i class="fas fa-book-open"></i></span>
        <span class="menu-text">Read Tracker</span>
      </div>
    </div>

    <div class="menu-items">
      <div
        class="menu-item"
        :class="{ active: currentPage === 'recommendations' }"
        @click="$emit('navigate', 'recommendations')"
      >
        <span class="menu-icon"><i class="fas fa-home"></i></span>
        <span class="menu-text">Main Page</span>
      </div>

      <div
        class="menu-item"
        :class="{ active: currentPage === 'profile' }"
        @click="$emit('navigate', 'profile')"
      >
        <span class="menu-icon"><i class="fas fa-user"></i></span>
        <span class="menu-text">My Profile</span>
      </div>

      <div
        class="menu-item"
        :class="{ active: currentPage === 'books' }"
        @click="$emit('navigate', 'books')"
      >
        <span class="menu-icon"><i class="fas fa-book"></i></span>
        <span class="menu-text">My Books</span>
      </div>

      <div
        class="menu-item"
        :class="{ active: currentPage === 'publicBooks' }"
        @click="$emit('navigate', 'publicBooks')"
      >
        <span class="menu-icon"><i class="fas fa-book-open"></i></span>
        <span class="menu-text">All Books</span>
      </div>

      <div
        class="menu-item"
        :class="{ active: currentPage === 'collections' }"
        @click="$emit('navigate', 'collections')"
      >
        <span class="menu-icon"><i class="fas fa-folder"></i></span>
        <span class="menu-text">My Collections</span>
      </div>

      <div
        class="menu-item"
        :class="{ active: currentPage === 'reviews' }"
        @click="$emit('navigate', 'reviews')"
      >
        <span class="menu-icon"><i class="fas fa-pen"></i></span>
        <span class="menu-text">My Reviews</span>
      </div>

      <div
        class="menu-item"
        :class="{ active: currentPage === 'subscriptions' }"
        @click="$emit('navigate', 'subscriptions')"
      >
        <span class="menu-icon"><i class="fas fa-user-friends"></i></span>
        <span class="menu-text">Subscriptions</span>
      </div>
    </div>

    <div class="bottom-menu">
      <div class="menu-item">
        <span class="menu-icon"><i class="fas fa-cog"></i></span>
        <span class="menu-text">Settings</span>
      </div>

      <div class="menu-item" @click="handleLogout">
        <span class="menu-icon"><i class="fas fa-sign-out-alt"></i></span>
        <span class="menu-text">Log Out</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'

const props = defineProps({
  isCollapsed: Boolean,
  currentPage: String
})

const authStore = useAuthStore()
const router = useRouter()

function handleLogout() {
  authStore.logout(router)
  router.push('/login')
}
</script>