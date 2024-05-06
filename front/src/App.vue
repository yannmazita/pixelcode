<template>
    <div class="grid grid-cols-12">
        <div class="col-span-12"></div>
        <NavBar class="col-span-12"></NavBar>
        <main class="col-span-12 h-[calc(100vh-64px)] p-3.5 lg:p-6">
            <router-view></router-view>
        </main>
    </div>
</template>

<script setup lang="ts">
import NavBar from '@/components/AppNavBar.vue'
</script>
