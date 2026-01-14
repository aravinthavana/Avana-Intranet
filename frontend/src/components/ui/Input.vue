<template>
  <div :class="['w-full', containerClass]">
    <label v-if="label" :for="id" class="block text-sm font-medium text-neutral-700 mb-1.5">
      {{ label }}
      <span v-if="required" class="text-error-500">*</span>
    </label>
    
    <div class="relative">
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :class="inputClasses"
        @input="$emit('update:modelValue', $event.target.value)"
        @blur="$emit('blur')"
        @focus="$emit('focus')"
      />
      
      <div v-if="$slots.suffix" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <slot name="suffix"></slot>
      </div>
    </div>
    
    <p v-if="error" class="mt-1.5 text-sm text-error-600 flex items-center gap-1">
      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
      </svg>
      {{ error }}
    </p>
    
    <p v-else-if="helper" class="mt-1.5 text-sm text-neutral-500">
      {{ helper }}
    </p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  id: String,
  modelValue: [String, Number],
  type: {
    type: String,
    default: 'text'
  },
  label: String,
  placeholder: String,
  error: String,
  helper: String,
  disabled: Boolean,
  required: Boolean,
  containerClass: String
})

defineEmits(['update:modelValue', 'blur', 'focus'])

const inputClasses = computed(() => {
  const base = 'block w-full px-3 py-2 border rounded-lg shadow-sm placeholder-neutral-400 focus:outline-none focus:ring-2 focus:ring-offset-0 transition-colors sm:text-sm'
  
  const state = props.error
    ? 'border-error-300 text-error-900 focus:ring-error-500 focus:border-error-500'
    : 'border-neutral-300 focus:ring-primary-500 focus:border-primary-500'
  
  const disabled = props.disabled
    ? 'bg-neutral-50 text-neutral-500 cursor-not-allowed'
    : 'bg-white'
  
  return [base, state, disabled].join(' ')
})
</script>
