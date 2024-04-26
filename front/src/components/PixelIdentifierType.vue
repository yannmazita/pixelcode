<template>
    <div class="flex justify-center">
        <span class="text-3xl">Email</span>
        <input @click="menuStore.setIdentifierTypeEmail(true)" class="mx-2 radio radio-primary" type="radio" name="radio-2"
            checked />
        <input @click="menuStore.setIdentifierTypeID(true)" class="mx-2 radio radio-primary" type="radio" name="radio-2" />
        <span class="text-3xl">id #</span>
    </div>
</template>
<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue';
import { useMenuStore } from '@/stores/menu.ts';
const menuStore = useMenuStore();

onMounted(() => {
    menuStore.setIdentifierTypeEmail(true);
});

onUnmounted(() => {
    menuStore.resetIdentifierChoices();
});
</script>
