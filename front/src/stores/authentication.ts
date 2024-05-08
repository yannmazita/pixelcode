import { defineStore } from 'pinia';
import { ref, reactive, Ref } from 'vue';
import axios from 'axios';
import type { TokenData, User } from '@/interfaces.ts';

export const useAuthenticationStore = defineStore('authentication', () => {
    const authenticated: Ref<boolean> = ref(false);
    const tokenData: TokenData = reactive({
        access_token: null,
        token_type: null,
    });
    const user: User = reactive({
        id: "",
        username: "",
        roles: "",
    });

    // This function is to be called when the user is already logged in.
    async function getOwnUser(): Promise<void> {
        try {
            const response = await axios.get(
                `${import.meta.env.VITE_API_URL}/users/me`,
                {
                    headers: {
                        accept: 'application/json',
                        Authorization: `Bearer ${tokenData.access_token}`,
                    }
                }
            );
            Object.assign(user, response.data);
        }
        catch (error) {
            console.error(error);
        }
    }

    // This function is called to log in the user.
    async function loginUser(formData: any): Promise<void> {
        console.log('Logging in user.');
        try {
            const response = await axios.post(
                `${import.meta.env.VITE_API_URL}/login/`,
                formData,
                {
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    }
                },
            );
            Object.assign(tokenData, response.data);
        }
        catch (error) {
            console.log(error);
        }

        try {
            console.log('Getting own user.');
            await getOwnUser();
            authenticated.value = true;
            console.log(user);
        }
        catch (error) {
            console.log(error);
        }
    }

    // This function is called to log out the user.
    async function logoutUser(): Promise<void> {
        try {
            // maybe use forEach or something
            tokenData.access_token = null;
            tokenData.token_type = null;
            user.id = "";
            user.username = "";
            authenticated.value = false;
        }
        catch (error) {
            console.log(error);
        }
    }

    // This function is called to register the user.
    async function registerUser(formData: any): Promise<void> {
        try {
            const response = await axios.post(
                `${import.meta.env.VITE_API_URL}/register/`,
                formData);
            Object.assign(tokenData, response.data);
            authenticated.value = true;
        }
        catch (error) {
            console.log(error);
        }
    }


    return {
        tokenData,
        loginUser,
        logoutUser,
        registerUser,
        getOwnUser,
        user,
        authenticated,
    }
})

