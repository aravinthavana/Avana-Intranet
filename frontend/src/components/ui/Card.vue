<template>
  <div :class="cardClasses">
    <div v-if="$slots.header || title" class="border-b border-neutral-200 pb-4 mb-4">
      <slot name="header">
        <h3 class="text-lg font-semibold text-neutral-900">{{ title }}</h3>
      </slot>
    </div>
    
    <div class="card-body">
      <slot></slot>
    </div>
    
    <div v-if="$slots.footer" class="border-t border-neutral-200 pt-4 mt-4">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: String,
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'bordered', 'elevated'].includes(value)
  },
  padding: {
    type: String,
    default: 'normal',
    validator: (value) => ['none', 'sm', 'normal', 'lg'].includes(value)
  },
  hoverable: Boolean
})

const cardClasses = computed(() => {
  const base = 'bg-white rounded-lg transition-all duration-200'
  
  const variants = {
    default: 'border border-neutral-200 shadow-card',
    bordered: 'border-2 border-neutral-300',
    elevated: 'shadow-lg'
  }
  
  const paddings = {
    none: '',
    sm: 'p-4',
    normal: 'p-6',
    lg: 'p-8'
  }
  
  const hover = props.hoverable ? 'hover:shadow-card-hover hover:-translate-y-0.5 cursor-pointer' : ''
  
  return [base, variants[props.variant], paddings[props.padding], hover].join(' ')
})
</script>
