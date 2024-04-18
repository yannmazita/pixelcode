import { defineStore } from 'pinia';
import { ref, Ref } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import { useAuthenticationStore } from '@/stores/authentication.ts';

export const useUserStore = defineStore('user', () => {
    const socket: Ref<WebSocket | null> = ref(null);
    const socketConnected: Ref<boolean> = ref(false);
    const socketError: Ref<Event | null> = ref(null);
    const socketMessage: Ref<any | null> = ref(null);

    const authStore = useAuthenticationStore();

    async function connectSocket(): Promise<void> {
        return new Promise((resolve, reject) => {
            const id: string = authStore.user.id ? authStore.user.id : uuidv4();
            const path: string = 'user';
            const queryParam: string = 'user_id';

            socket.value = new WebSocket(
                `${import.meta.env.VITE_WS_URL}/${path}?${queryParam}=${id}`
            );
            socket.value.onopen = () => {
                socketConnected.value = true;
                sendTokenData();
                console.log('(user) Websocket connected.');
                resolve();
            };
            socket.value.onerror = (error) => {
                socketError.value = error;
                console.log(error);
                reject(error);
            };
            socket.value.onmessage = (message) => {
                socketMessage.value = JSON.parse(message.data.toString());
                console.log('(user) Message received: ', socketMessage.value);
            };
            socket.value.onclose = () => {
                socketConnected.value = false;
                console.log('(user) Websocket closed.');
            };
        });
    }

    async function disconnectSocket(): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
                socket.value?.close();
                console.log('(user) Websocket disconnected.');
                resolve();
            }
            catch (error) {
                console.log(error);
                reject(error);
            }
        });
    }

    async function sendSocketMessage(message: string): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
                socket.value?.send(message);
                console.log('(user) Message sent: ', message);
                resolve();
            }
            catch (error) {
                console.log(error);
                reject(error);
            }
        });
    }

    function resetSocket(): void {
        socket.value = null;
        socketConnected.value = false;
        socketError.value = null;
        socketMessage.value = null;
    }

    async function sendTokenData(): Promise<void> {
        return new Promise(async (reolve, reject) => {
            try {
                await sendSocketMessage(JSON.stringify({
                    action: 'token_data',
                    data: authStore.tokenData,
                }));
                reolve();
            }
            catch (error) {
                console.log(error);
                reject(error);
            }
        });
    }

    return {
        socketConnected,
        socketError,
        socketMessage,
        connectSocket,
        disconnectSocket,
        sendSocketMessage,
        resetSocket,
    }
});
