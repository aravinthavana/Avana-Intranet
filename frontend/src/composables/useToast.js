import { ref, h, render } from 'vue'
import Toast from '../components/ui/Toast.vue'

const toasts = ref([])

export function useToast() {
    function show(options) {
        const {
            type = 'info',
            title,
            message,
            duration = 5000
        } = typeof options === 'string' ? { message: options } : options

        const id = Date.now()
        const container = document.createElement('div')
        container.id = `toast-${id}`
        document.body.appendChild(container)

        const vnode = h(Toast, {
            type,
            title,
            message,
            duration,
            onClose: () => {
                render(null, container)
                document.body.removeChild(container)
                toasts.value = toasts.value.filter(t => t.id !== id)
            }
        })

        render(vnode, container)

        const toast = { id, type, message }
        toasts.value.push(toast)

        return id
    }

    function success(message, title) {
        return show({ type: 'success', message, title })
    }

    function error(message, title) {
        return show({ type: 'error', message, title })
    }

    function warning(message, title) {
        return show({ type: 'warning', message, title })
    }

    function info(message, title) {
        return show({ type: 'info', message, title })
    }

    return {
        show,
        success,
        error,
        warning,
        info,
        toasts
    }
}
