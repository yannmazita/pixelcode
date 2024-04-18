<template>
    <div class="grid grid-cols-12">
        <div class="col-span-12"></div>
        <NavBar class="col-span-12"></NavBar>
        <main class="col-span-12 h-[calc(100vh-64px)] p-5">
            <router-view></router-view>
        </main>
    </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/AppNavBar.vue'
import { onMounted } from 'vue';
import { useClientStore } from '@/stores/client.ts';

const clientStore = useClientStore();

onMounted(async () => {
    try {
        await clientStore.connectSocket();
        await clientStore.sendSocketMessage(JSON.stringify({
            action: 'server_stats',
            data: null
        }));
    } catch (error) {
        console.log(error)
    }
});
</script>
