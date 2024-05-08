import { ref, Ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useAuthenticationStore } from '@/stores/authentication.ts';
import { User, UserCreate } from '@/interfaces.ts';

export const useUserStore = defineStore('user', () => {
    const users: Ref<User[]> = ref([]);
    const totalUsers: Ref<number> = ref(0);

    async function getUsers(offset: number = 0, limit: number = 25): Promise<void> {
        const authenticationStore = useAuthenticationStore();
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/users/all`, {
                headers: { Authorization: `Bearer ${authenticationStore.tokenData.access_token}` },
                params: { offset, limit },
            });
            users.value = response.data[0];
            totalUsers.value = response.data[1];
        } catch (error) {
            console.error('Failed to get users:', error);
        }
    };
    async function addUser(userData: UserCreate): Promise<void> {
        const authenticationStore = useAuthenticationStore();
        try {
            await axios.post(`${import.meta.env.VITE_API_URL}/users/`, userData, {
                headers: { Authorization: `Bearer ${authenticationStore.tokenData.access_token}` }
            });
        } catch (error) {
            console.error('Failed to add user:', error);
        }
    };
    async function updateUser(id: string, userData: UserCreate): Promise<void> {
        const authenticationStore = useAuthenticationStore();
        try {
            await axios.put(`${import.meta.env.VITE_API_URL}/users/id/${id}`, userData, {
                headers: { Authorization: `Bearer ${authenticationStore.tokenData.access_token}` }
            });
        } catch (error) {
            console.error('Failed to update user:', error);
        }
    };
    async function updateUserUsername(id: string, username: string): Promise<void> {
        const authenticationStore = useAuthenticationStore();
        try {
            await axios.patch(`${import.meta.env.VITE_API_URL}/users/id/${id}/username`, { username }, {
                headers: { Authorization: `Bearer ${authenticationStore.tokenData.access_token}` }
            });
        } catch (error) {
            console.error('Failed to update user username:', error);
        }
    }
    async function updateUserRoles(id: string, roles: string): Promise<void> {
        const authenticationStore = useAuthenticationStore();
        try {
            await axios.patch(`${import.meta.env.VITE_API_URL}/users/id/${id}/roles`, { roles }, {
                headers: { Authorization: `Bearer ${authenticationStore.tokenData.access_token}` }
            });
        } catch (error) {
            console.error('Failed to update user roles:', error);
        }
    };
    async function deleteUser(id: string): Promise<void> {
        const authenticationStore = useAuthenticationStore();
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}/users/id/${id}`, {
                headers: { Authorization: `Bearer ${authenticationStore.tokenData.access_token}` }
            });
        } catch (error) {
            console.error('Failed to delete user:', error);
        }
    }
    return {
        users,
        totalUsers,
        getUsers,
        addUser,
        updateUser,
        updateUserUsername,
        updateUserRoles,
        deleteUser,
    }
})
