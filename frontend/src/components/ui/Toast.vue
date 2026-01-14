<template>
  <Teleport to="body">
    <Transition name="toast">
      <div
        v-if="visible"
        :class="toastClasses"
        role="alert"
        @click="close"
      >
        <div class="flex items-start gap-3">
          <div class="flex-shrink-0">
            <component :is="iconComponent" class="w-5 h-5" />
          </div>
          
          <div class="flex-1 pt-0.5">
            <p v-if="title" class="font-semibold text-sm">{{ title }}</p>
            <p class="text-sm" :class="{ 'mt-1': title }">{{ message }}</p>
          </div>
          
          <button
            @click.stop="close"
            class="flex-shrink-0 ml-4 inline-flex text-current hover:opacity-75 focus:outline-none"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  title: String,
  message: {
    type: String,
    required: true
  },
  duration: {
    type: Number,
    default: 5000
  }
})

const emit = defineEmits(['close'])

const visible = ref(false)
let timer = null

const toastClasses = computed(() => {
  const base = 'fixed top-4 right-4 max-w-sm w-full shadow-lg rounded-lg p-4 pointer-events-auto z-50'
  
  const types = {
    success: 'bg-success-50 text-success-800 border border-success-200',
    error: 'bg-error-50 text-error-800 border border-error-200',
    warning: 'bg-warning-50 text-warning-800 border border-warning-200',
    info: 'bg-blue-50 text-blue-800 border border-blue-200'
  }
  
  return [base, types[props.type]].join(' ')
})

const iconComponent = computed(() => {
  const icons = {
    success: () => h('svg', { class: 'w-5 h-5', fill: 'currentColor', viewBox: '0 0 20 20' }, [
      h('path', { 'fill-rule': 'evenodd', d: 'M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z', 'clip-rule': 'evenodd' })
    ]),
    error: () => h('svg', { class: 'w-5 h-5', fill: 'currentColor', viewBox: '0 0 20 20' }, [
      h('path', { 'fill-rule': 'evenodd', d: 'M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z', 'clip-rule': 'evenodd' })
    ]),
    warning: () => h('svg', { class: 'w-5 h-5', fill: 'currentColor', viewBox: '0 0 20 20' }, [
      h('path', { 'fill-rule': 'evenodd', d: 'M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z', 'clip-rule': 'evenodd' })
    ]),
    info: () => h('svg', { class: 'w-5 h-5', fill: 'currentColor', viewBox: '0 0 20 20' }, [
      h('path', { 'fill-rule': 'evenodd', d: 'M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z', 'clip-rule': 'evenodd' })
    ])
  }
  
  return icons[props.type]
})

function close() {
  visible.value = false
  if (timer) clearTimeout(timer)
  setTimeout(() => emit('close'), 300)
}

onMounted(() => {
  visible.value = true
  
  if (props.duration > 0) {
    timer = setTimeout(close, props.duration)
  }
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
