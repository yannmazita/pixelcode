<template>
    <div class="grid grid-flow-row h-full max-w-full">
    <Login v-if="!authenticated"></Login>
    <AdminDashboard v-else></AdminDashboard>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia'
import { useAuthenticationStore } from '@/stores/authentication.ts'
import Login from '@/components/AppLoginHero.vue'
import AdminDashboard from '@/components/AppAdminDashboard.vue'

const authenticationStore = useAuthenticationStore();
const authenticated = computed(() => {
    return authenticationStore.authenticated;
});
</script>
