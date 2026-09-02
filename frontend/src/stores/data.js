import { defineStore } from 'pinia'
import { ref } from 'vue'
export const useDataStore = defineStore('data', () => {
    const intercom = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Auth state is verified on initialization via checkAuth()
    const isAuthenticatedState = ref(false)

    const API_BASE = import.meta.env.VITE_API_URL || '/api'

    // ────────────────────────────────────────────────
    // Token Helpers
    // ────────────────────────────────────────────────
    function getAuthHeaders() {
        return {
            'Content-Type': 'application/json'
        }
    }

    // ────────────────────────────────────────────────
    // Response Helper
    // ────────────────────────────────────────────────
    async function handleResponse(response) {
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}))
            const errorMessage = errorData.error || errorData.message || `HTTP ${response.status}`

            if (response.status === 401) {
                isAuthenticatedState.value = false
                throw new Error('Session expired. Please log in again.')
            }

            throw new Error(errorMessage)
        }
        return response.json()
    }

    // ────────────────────────────────────────────────
    // Data Fetching
    // ────────────────────────────────────────────────
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
        const res = await fetch(`${API_BASE}/intercom`)
        const json = await handleResponse(res)
        intercom.value = json.data || []
    }

    // ────────────────────────────────────────────────
    // Admin CRUD
    // ────────────────────────────────────────────────
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
            await fetchIntercom()
            return true
        } catch (e) {
            error.value = e.message
            throw e
        } finally {
            loading.value = false
        }
    }

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
            throw e
        } finally {
            loading.value = false
        }
    }

    async function deleteIntercom(id) {
        loading.value = true
        try {
            const res = await fetch(`${API_BASE}/intercom/${id}`, {
                method: 'DELETE',
                credentials: 'include',
                headers: getAuthHeaders()
            })
            await handleResponse(res)
            await fetchIntercom()
            return true
        } catch (e) {
            error.value = e.message
            throw e
        } finally {
            loading.value = false
        }
    }

    async function changePassword(oldPassword, newPassword) {
        loading.value = true
        try {
            const res = await fetch(`${API_BASE}/change-password`, {
                method: 'PUT',
                headers: getAuthHeaders(),
                credentials: 'include',
                body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
            })
            const data = await handleResponse(res)
            return data.success
        } catch (e) {
            error.value = e.message
            throw e
        } finally {
            loading.value = false
        }
    }

    // ────────────────────────────────────────────────
    // Auth
    // ────────────────────────────────────────────────
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

            // The backend sets the HTTP-Only cookie automatically.
            // We just need to trust the success response.
            if (data.success) {
                isAuthenticatedState.value = true
            }
            return true
        } catch (e) {
            error.value = e.message
            isAuthenticatedState.value = false
            throw e
        } finally {
            loading.value = false
        }
    }

    async function logout() {
        try {
            await fetch(`${API_BASE}/logout`, {
                method: 'POST',
                credentials: 'include',
                headers: getAuthHeaders()
            })
        } catch (e) {
            console.error('Logout request failed:', e)
        } finally {
            isAuthenticatedState.value = false
        }
    }

    function isAuthenticated() {
        return isAuthenticatedState.value
    }

    async function checkAuth() {
        try {
            const res = await fetch(`${API_BASE}/check-auth`, {
                method: 'GET',
                credentials: 'include'
            })
            if (res.ok) {
                const data = await res.json()
                isAuthenticatedState.value = !!data.authenticated
            } else {
                isAuthenticatedState.value = false
            }
        } catch (e) {
            isAuthenticatedState.value = false
            console.error('Check auth failed:', e)
        }
    }

    return {
        intercom,
        loading,
        error,
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
