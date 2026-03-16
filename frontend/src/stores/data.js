import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDataStore = defineStore('data', () => {
    const intercom = ref([])
    const loading = ref(false)
    const error = ref(null)
    // Auth state is now boolean, not token based
    const isAuthenticatedState = ref(false)

    // Base URL: Use env var if set (e.g. for separate hosting), otherwise relative path (for same-origin serving)
    const API_BASE = import.meta.env.VITE_API_URL || '/api'

    /**
     * Get headers for authenticated requests
     * (Cookies are handled automatically by browser)
     */
    function getAuthHeaders() {
        return {
            'Content-Type': 'application/json'
        }
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
                isAuthenticatedState.value = false
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
            await fetchIntercom()
        } catch (e) {
            error.value = e.message
            console.error('Failed to fetch data:', e)
        } finally {
            loading.value = false
        }
    }

    async function fetchIntercom() {
        try {
            const res = await fetch(`${API_BASE}/intercom`, { credentials: 'include' })
            const json = await handleResponse(res)
            intercom.value = json.data || [] // Handle wrapped response
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
                credentials: 'include',
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
                credentials: 'include',
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
                headers: getAuthHeaders(),
                credentials: 'include'
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
     * Login and set HttpOnly cookie
     */
    async function login(password) {
        loading.value = true
        error.value = null

        try {
            const res = await fetch(`${API_BASE}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include',
                body: JSON.stringify({ password })
            })

            const data = await handleResponse(res)

            // Success (Cookie is set by server)
            isAuthenticatedState.value = true
            return true
        } catch (e) {
            error.value = e.message
            console.error('Login failed:', e)
            isAuthenticatedState.value = false // Ensure state is synced
            throw e
        } finally {
            loading.value = false
        }
    }

    /**
     * Logout and clear cookie
     */
    async function logout() {
        try {
            await fetch(`${API_BASE}/logout`, { method: 'POST', credentials: 'include' })
        } catch (e) {
            console.error('Logout failed (network error?):', e)
        } finally {
            isAuthenticatedState.value = false
        }
    }

    /**
     * Check if session is valid from server
     */
    async function checkAuth() {
        // Only verify with server if we think we are already authenticated
        // This prevents resetting auth state on every page load due to cookie issues
        if (!isAuthenticatedState.value) return
        try {
            const res = await fetch(`${API_BASE}/check-auth`, {
                credentials: 'include'
            })
            if (res.ok) {
                const data = await res.json()
                // Only clear auth if server explicitly says not authenticated
                if (!data.authenticated) {
                    isAuthenticatedState.value = false
                }
            }
            // If request fails (network error), keep current state
        } catch (e) {
            // Network error - keep current auth state, don't log out
            console.warn('checkAuth network error, keeping current state:', e)
        }
    }

    /**
     * Check if user is authenticated (Frontend check)
     */
    function isAuthenticated() {
        return isAuthenticatedState.value
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
        checkAuth,
        changePassword,
        isAuthenticated
    }
})
