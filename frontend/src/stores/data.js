import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDataStore = defineStore('data', () => {
    const intercom = ref([])
    const loading = ref(false)
    const error = ref(null)
    // Make token reactive so UI updates immediately
    const token = ref(localStorage.getItem('admin_token'))

    // Base URL is relative
    const API_BASE = '/api'

    /**
     * Get headers for authenticated requests
     */
    function getAuthHeaders() {
        const headers = {
            'Content-Type': 'application/json'
        }

        if (token.value) {
            headers['Authorization'] = `Bearer ${token.value}`
        }

        return headers
    }

    /**
     * Handle API errors with proper status code checking
     */
    async function handleResponse(response) {
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}))
            const errorMessage = errorData.error || errorData.message || `HTTP ${response.status}`

            // Handle authentication errors
            if (response.status === 401) {
                localStorage.removeItem('admin_token')
                token.value = null
                throw new Error('Authentication required. Please log in again.')
            }

            throw new Error(errorMessage)
        }

        return response.json()
    }

    /**
     * Fetch all public data
     */
    async function fetchAll() {
        loading.value = true
        error.value = null

        try {
            await Promise.all([
                fetchIntercom()
            ])
        } catch (e) {
            error.value = e.message
            console.error('Failed to fetch data:', e)
        } finally {
            loading.value = false
        }
    }

    async function fetchIntercom() {
        try {
            const res = await fetch(`${API_BASE}/intercom`)
            intercom.value = await handleResponse(res)
        } catch (e) {
            console.error('Failed to fetch intercom:', e)
            throw e
        }
    }

    /**
     * Add new person
     */
    async function addIntercom(person) {
        loading.value = true
        try {
            const res = await fetch(`${API_BASE}/intercom`, {
                method: 'POST',
                headers: getAuthHeaders(),
                body: JSON.stringify(person)
            })
            await handleResponse(res)
            await fetchIntercom() // Refresh list
            return true
        } catch (e) {
            error.value = e.message
            console.error('Add failed:', e)
            throw e
        } finally {
            loading.value = false
        }
    }

    /**
     * Update existing person
     */
    async function updateIntercom(id, person) {
        loading.value = true
        try {
            const res = await fetch(`${API_BASE}/intercom/${id}`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify(person)
            })
            await handleResponse(res)
            await fetchIntercom()
            return true
        } catch (e) {
            error.value = e.message
            console.error('Update failed:', e)
            throw e
        } finally {
            loading.value = false
        }
    }

    /**
     * Delete person
     */
    async function deleteIntercom(id) {
        loading.value = true
        try {
            const res = await fetch(`${API_BASE}/intercom/${id}`, {
                method: 'DELETE',
                headers: getAuthHeaders()
            })
            await handleResponse(res)
            await fetchIntercom()
            return true
        } catch (e) {
            error.value = e.message
            console.error('Delete failed:', e)
            throw e
        } finally {
            loading.value = false
        }
    }

    /**
     * Change admin password
     */
    async function changePassword(oldPassword, newPassword) {
        loading.value = true
        try {
            const res = await fetch(`${API_BASE}/change-password`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
            })
            const data = await handleResponse(res)
            return data.success
        } catch (e) {
            error.value = e.message
            console.error('Password change failed:', e)
            throw e
        } finally {
            loading.value = false
        }
    }

    /**
     * Login and get JWT token
     */
    async function login(password) {
        loading.value = true
        error.value = null

        try {
            const res = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            })

            const data = await handleResponse(res)

            if (data.token) {
                localStorage.setItem('admin_token', data.token)
                token.value = data.token
                return true
            }

            return false
        } catch (e) {
            error.value = e.message
            console.error('Login failed:', e)
            throw e
        } finally {
            loading.value = false
        }
    }

    /**
     * Logout and clear token
     */
    function logout() {
        localStorage.removeItem('admin_token')
        token.value = null
    }

    /**
     * Check if user is authenticated
     */
    function isAuthenticated() {
        return !!token.value
    }

    return {
        // State
        intercom,
        loading,
        error,

        // Methods
        fetchAll,
        fetchIntercom,
        addIntercom,
        updateIntercom,
        deleteIntercom,
        login,
        logout,
        changePassword,
        isAuthenticated
    }
})
