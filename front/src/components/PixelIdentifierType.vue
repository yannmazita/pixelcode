<template>
    <div class="flex justify-center">
        <span class="text-2xl">Email</span>
        <input @click="searchStore.setSearchByEmail()" class="mx-2 radio radio-primary" type="radio" name="radio-2"
            checked />
        <input @click="searchStore.setSearchById()" class="mx-2 radio radio-primary" type="radio" name="radio-2" />
        <span class="text-2xl">id #</span>
    </div>
</template>
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';
import { useSearchStore } from '@/stores/search.ts';
const searchStore = useSearchStore();

onMounted(() => {
    searchStore.setSearchByEmail();
});

onUnmounted(() => {
    searchStore.clearSearch();
});
</script>
