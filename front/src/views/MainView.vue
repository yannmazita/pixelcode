<template>
    <div class="grid grid-flow-row h-full max-w-full">
        <PageTitle>{{ currentPage }}</PageTitle>
        <component :is="visibleComponent"></component>
    </div>
</template>
<script setup lang="ts">
import { useMenuStore } from '@/stores/menu.ts';
import { computed, onMounted } from 'vue';
import { storeToRefs } from 'pinia';
import { PageType } from '@/enums.ts';
import HomeView from '@/views/HomeView.vue';
import FindEmployee from '@/views/FindEmployeeView.vue';
import VerificationCode from '@/views/VerificationCode.vue';
import PageTitle from '@/components/AppPageTitle.vue';

const menuStore = useMenuStore();
const { currentPage } = storeToRefs(menuStore);

const visibleComponent = computed(() => {
    if (menuStore.currentPage === PageType.FIND_EMPLOYEE) {
        return FindEmployee;
    }
    else if (menuStore.currentPage === PageType.VERIFICATION_CODE) {
        return VerificationCode;
    }
    else {
        return HomeView;
    }

});

onMounted(() => {
    menuStore.setCurrentPage(PageType.HOME);
});
</script>
