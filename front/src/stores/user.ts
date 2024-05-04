import { ref, Ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useAuthenticationStore } from '@/stores/authentication.ts';
import { User, UserCreate } from '@/interfaces.ts';

export const useUserStore = defineStore('user', () => {
    const users: Ref<User[]> = ref([]);

    async function getUsers(): Promise<void> {
        const authenticationStore = useAuthenticationStore();
        try {
            const response = await axios.get(`${import.meta.env.VITE_API_URL}/users/all`, {
                headers: { Authorization: `Bearer ${authenticationStore.tokenData.access_token}` }
            });
            users.value = response.data;
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
            await getUsers();
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
            await getUsers();
        } catch (error) {
            console.error('Failed to update user:', error);
        }
    };
    async function deleteUser(id: string): Promise<void> {
        const authenticationStore = useAuthenticationStore();
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}/users/id/${id}`, {
                headers: { Authorization: `Bearer ${authenticationStore.tokenData.access_token}` }
            });
            await getUsers();
        } catch (error) {
            console.error('Failed to delete user:', error);
        }
    }
    return {
        users,
        getUsers,
        addUser,
        updateUser,
        deleteUser,
    }
})
