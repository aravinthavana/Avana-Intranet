<template>
  <div class="card" style="max-width: 400px; width: 100%;">
    <h2>Admin Login</h2>
    <form @submit.prevent="handleLogin">
       <input 
         v-model="password" 
         type="password" 
         placeholder="Password" 
         :disabled="store.loading"
         required
       />
       <button type="submit" :disabled="store.loading">
         {{ store.loading ? 'Logging in...' : 'Login' }}
       </button>
       <p v-if="error" style="color:red; margin-top:10px;">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'

const password = ref('')
const error = ref('')
const router = useRouter()
const store = useDataStore()

async function handleLogin() {
  error.value = ''
  
  try {
    await store.login(password.value)
    // Login successful, navigate to dashboard
    router.push('/admin/dashboard')
  } catch (e) {
    error.value = e.message || 'Login failed. Please check your password.'
  }
}
</script>
