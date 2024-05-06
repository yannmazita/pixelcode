<template>
    <div class="grid grid-flow-row h-full max-w-full">
        <PageTitle>{{ currentPage }}</PageTitle>
        <component :is="visibleComponent"></component>
    </div>
</template>
<script setup lang="ts">
import HomeView from '@/views/HomeView.vue';
import FindEmployee from '@/views/FindEmployeeView.vue'
import VerificationCode from '@/views/VerificationCode.vue'
import PageTitle from '@/components/AppPageTitle.vue'
import { useMenuStore } from '@/stores/menu.ts';
import { computed } from 'vue';
import { storeToRefs } from 'pinia';

const menuStore = useMenuStore();
const { currentPageTitle: currentPage, } = storeToRefs(menuStore);

const visibleComponent = computed(() => {
    if (menuStore.findEmployeeChoice) {
        return FindEmployee;
    }
    else if (menuStore.codeChoice) {
        return VerificationCode;
    }
    else {
        return HomeView;
    }

});
</script>
