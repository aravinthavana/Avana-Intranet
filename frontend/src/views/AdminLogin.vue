<template>
  <div class="card" style="max-width: 400px; width: 100%;">
    <h2>Admin Login</h2>
    <form @submit.prevent="handleLogin">
       <input v-model="password" type="password" placeholder="Password" />
       <button type="submit">Login</button>
       <p v-if="error" style="color:red; margin-top:10px;">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const password = ref('')
const error = ref('')
const router = useRouter()

async function handleLogin() {
  // Simple check against backend
  try {
      const res = await fetch('/api/login', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ password: password.value })
      })
      const data = await res.json()
      if (data.success) {
          localStorage.setItem('admin_token', data.token)
          router.push('/admin/dashboard')
      } else {
          error.value = 'Invalid password'
      }
  } catch (e) {
      // Allow bypass if offline for testing? No, stick to logic.
      // If server is down, this will fail.
      error.value = 'Login failed (Server error)'
  }
}
</script>
