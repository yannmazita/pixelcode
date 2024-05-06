<template>
    <div class="navbar bg-base-300 h-fit w-full py-0">
        <div class="navbar-start">
            <router-link to="/" @click="menuStore.resetPage()" class="btn btn-ghost text-2xl xl:text-5xl">pixelcode</router-link>
        </div>

        <div class="navbar-end text-4xl">
            <router-link to="/" @click="menuStore.resetPage()" v-if="showBackButton" class="btn btn-ghost text-2xl xl:text-3xl">↩️</router-link>
            <router-link to="/admin" @click="menuStore.setCurrentPage(PageType.ADMIN)" class="btn btn-ghost text-2xl xl:text-3xl">🔒</router-link>
            <router-link to="/help" @click="menuStore.setCurrentPage(PageType.HELP)" class="btn btn-ghost text-2xl xl:text-3xl">❔</router-link>
        </div>
    </div>
</template>


<script setup lang="ts">
import { computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useMenuStore } from '@/stores/menu.ts';
import { PageType } from '@/enums.ts';

const menuStore = useMenuStore();
const { currentPage } = storeToRefs(menuStore);

const showBackButton = computed(() => {
    return currentPage.value !== PageType.HOME;
});
</script>
