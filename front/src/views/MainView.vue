<template>
    <div class="grid grid-flow-row h-full max-w-full">
        <PageTitle>{{ currentPage }}</PageTitle>
        <component :is="visibleComponent"></component>
    </div>
</template>
<script setup lang="ts">
import HomeView from '@/views/HomeView.vue';
import FindEmployee from '@/views/FindEmployeeView.vue'
import PageTitle from '@/components/AppPageTitle.vue'
import { useMenuStore } from '@/stores/menu.ts';
import { computed } from 'vue';

const menuStore = useMenuStore();

const currentPage = computed(() => {
    return menuStore.currentPageTitle;
});

const visibleComponent = computed(() => {
    if (menuStore.informationChoice) {
        return FindEmployee;
    }
    else if (menuStore.codeChoice) {
        return;
    }
    else {
        return HomeView;
    }

});
</script>
