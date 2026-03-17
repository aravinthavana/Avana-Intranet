import { defineStore } from 'pinia'
import { ref } from 'vue'

const TOKEN_KEY = 'avana_admin_token'

export const useDataStore = defineStore('data', () => {
    const intercom = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Auth state is driven purely from localStorage token
    const isAuthenticatedState = ref(!!localStorage.getItem(TOKEN_KEY))

    const API_BASE = import.meta.env.VITE_API_URL || '/api'

    // ────────────────────────────────────────────────
    // Token Helpers
    // ────────────────────────────────────────────────
    function getToken() {
        return localStorage.getItem(TOKEN_KEY)
    }

    function setToken(token) {
        localStorage.setItem(TOKEN_KEY, token)
        isAuthenticatedState.value = true
    }

    function clearToken() {
        localStorage.removeItem(TOKEN_KEY)
        isAuthenticatedState.value = false
    }

    function getAuthHeaders() {
        const token = getToken()
        return {
            'Content-Type': 'application/json',
            ...(token ? { 'Authorization': `Bearer ${token}` } : {})
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
                clearToken()
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

            // Store the token in localStorage — no cookie dependency
            if (data.token) {
                setToken(data.token)
            } else {
                // Fallback: mark as authenticated even if no token in body
                isAuthenticatedState.value = true
                localStorage.setItem(TOKEN_KEY, 'authenticated')
            }
            return true
        } catch (e) {
            error.value = e.message
            clearToken()
            throw e
        } finally {
            loading.value = false
        }
    }

    async function logout() {
        try {
            const token = getToken()
            await fetch(`${API_BASE}/logout`, {
                method: 'POST',
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            })
        } catch (e) {
            console.error('Logout request failed:', e)
        } finally {
            clearToken()
        }
    }

    function isAuthenticated() {
        return isAuthenticatedState.value
    }

    // Kept for compatibility — no longer calls server
    async function checkAuth() {}

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
