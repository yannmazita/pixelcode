import { defineStore } from 'pinia';
import { ref, Ref } from 'vue';
import { v4 as uuidv4 } from 'uuid';

export const useClientStore = defineStore('client', () => {
    const socket: Ref<WebSocket | null> = ref(null);
    const socketConnected: Ref<boolean> = ref(false);
    const socketError: Ref<Event | null> = ref(null);
    const socketMessage: Ref<any | null> = ref(null);

    async function connectSocket(): Promise<void> {
        return new Promise((resolve, reject) => {
            const id: string = uuidv4();
            const path: string = 'client';
            const queryParam: string = 'client_id';

            socket.value = new WebSocket(
                `${import.meta.env.VITE_WS_URL}/${path}?${queryParam}=${id}`
            );
            socket.value.onopen = () => {
                socketConnected.value = true;
                console.log('(client) Websocket connected.');
                resolve();
            };
            socket.value.onerror = (error) => {
                socketError.value = error;
                console.log(error);
                reject(error);
            };
            socket.value.onmessage = (message) => {
                socketMessage.value = JSON.parse(message.data.toString());
                console.log('(client) Message received: ', socketMessage.value);
            };
            socket.value.onclose = () => {
                socketConnected.value = false;
                console.log('(client) Websocket closed.');
            };
        });
    }

    async function disconnectSocket(): Promise<void> {
        return new Promise((resolve, reject) => {
            try {
                socket.value?.close();
                console.log('(client) Websocket disconnected.');
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
                console.log('(client) Message sent: ', message);
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
