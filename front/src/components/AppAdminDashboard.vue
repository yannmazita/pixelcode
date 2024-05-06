<template>
    <div id="admin-dashboard-container" class="flex flex-col h-full">
        <h1 class="text-3xl font-bold">Admin Dashboard</h1>
        <UserList></UserList>
    </div>
</template>

<script setup lang="ts">
import UserList from '@/components/AppUserList.vue';
</script>
