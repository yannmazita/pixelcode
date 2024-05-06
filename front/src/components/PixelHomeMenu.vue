<template>
    <menu id="pixel-home-menu-container">
        <div id="pixel-home-menu" class="grid grid-flow-row">
            <li id="pixel-home-menu-information-choice" class="flex justify-center m-5">
                <AppButton @click="menuStore.setCurrentPage(PageType.FIND_EMPLOYEE)" class="">{{ 'Find employee' }}</AppButton>
            </li>
            <li id="pixel-home-menu-code-choice" class="flex justify-center m-5">
                <AppButton @click="menuStore.setCurrentPage(PageType.VERIFICATION_CODE)">{{ 'Verification code' }}</AppButton>
            </li>
        </div>
    </menu>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useMenuStore } from '@/stores/menu.ts'
import { usePixelStore } from '@/stores/pixel.ts'
import AppButton from '@/components/AppButton.vue';
import { PageType } from '@/enums.ts';

const menuStore = useMenuStore();
const pixelStore = usePixelStore();

onMounted(() => {
    menuStore.resetPage();
    pixelStore.resetEmployeeState();
});
</script>
