<template>
  <Card class="w-full max-w-md" padding="lg">
    <div class="text-center mb-6">
      <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
        <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
        </svg>
      </div>
      <h2 class="text-2xl font-bold text-neutral-900 mb-2">Admin Login</h2>
      <p class="text-sm text-neutral-600">Enter your password to access the admin dashboard</p>
    </div>
    
    <form @submit.prevent="handleLogin" class="space-y-4">
      <Input
        v-model="password"
        :type="showPassword ? 'text' : 'password'"
        label="Password"
        placeholder="Enter admin password"
        :error="error"
        :disabled="store.loading"
        required
        id="admin-password"
      >
        <template #suffix>
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="text-neutral-400 hover:text-neutral-600 focus:outline-none pointer-events-auto"
            tabindex="-1"
          >
            <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
            </svg>
            <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"/>
            </svg>
          </button>
        </template>
      </Input>
      
      <Button
        type="submit"
        :loading="store.loading"
        :disabled="!password || store.loading"
        full-width
        size="lg"
      >
        {{ store.loading ? 'Logging in...' : 'Login' }}
      </Button>
    </form>
    
    <div class="mt-6 text-center">
      <p class="text-xs text-neutral-500">
        Default password: <code class="px-1.5 py-0.5 bg-neutral-100 rounded text-neutral-700">admin123</code>
      </p>
    </div>
  </Card>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useDataStore } from '../stores/data'
import Button from '../components/ui/Button.vue'
import Input from '../components/ui/Input.vue'
import Card from '../components/ui/Card.vue'

const password = ref('')
const error = ref('')
const showPassword = ref(false)
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
