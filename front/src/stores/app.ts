import { defineStore } from 'pinia'
import { reactive } from 'vue'
import { useUserStore } from '@/stores/user.ts';
import { ServerStats } from '@/interfaces.ts';

export const useAppStore = defineStore('app', () => {
    const serverStats: ServerStats = reactive({
        active_users: 0,
    });
    const userStore = useUserStore();

    async function getServerStats() {
        userStore.sendSocketMessage(JSON.stringify({
            action: 'server_stats',
        }));
    };

    return {
        serverStats,
        getServerStats,
    }
})

