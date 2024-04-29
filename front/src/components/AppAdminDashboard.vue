<template>
    <div class="admin-panel">
        <h1 class="text-3xl font-bold">Admin Dashboard</h1>
        <UserManagement></UserManagement>
        <EmployeeManagement></EmployeeManagement>
    </div>
</template>

<script setup lang="ts">
import UserManagement from '@/components/AppUserManagement.vue';
import EmployeeManagement from '@/components/PixelEmployeeManagement.vue';
</script>
