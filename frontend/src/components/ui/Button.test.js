import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Button from './Button.vue'

describe('Button', () => {
    it('renders correctly', () => {
        const wrapper = mount(Button, {
            slots: {
                default: 'Click Me'
            }
        })
        expect(wrapper.text()).toContain('Click Me')
    })

    it('emits click event', async () => {
        const wrapper = mount(Button)
        await wrapper.trigger('click')
        expect(wrapper.emitted('click')).toBeTruthy()
    })

    it('applies variant classes', () => {
        const wrapper = mount(Button, {
            props: {
                variant: 'danger'
            }
        })
        expect(wrapper.classes()).toContain('bg-error-600')
    })

    it('shows loading state', () => {
        const wrapper = mount(Button, {
            props: {
                loading: true
            }
        })
        expect(wrapper.find('svg').exists()).toBe(true)
        expect(wrapper.attributes('disabled')).toBeDefined()
    })
})
