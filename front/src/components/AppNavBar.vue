<template>
    <div class="navbar bg-base-300 h-fit w-full py-0">
        <div class="navbar-start">
            <router-link to="/" @click="menuStore.resetChoices()" class="btn btn-ghost text-5xl">pixelcode</router-link>
        </div>

        <div class="navbar-end text-4xl">
            <router-link to="/" @click="goBack" v-if="showBackButton" class="btn btn-ghost text-5xl">↩️</router-link>
            <router-link to="/help" @click="helpChoice" class="btn btn-ghost text-5xl">❔</router-link>
        </div>
    </div>
</template>


<script setup lang="ts">
import { computed } from 'vue';
import { useMenuStore } from '@/stores/menu.ts';

const menuStore = useMenuStore();

const showBackButton = computed(() => {
    return menuStore.findEmployeeChoice || menuStore.codeChoice || menuStore.helpChoice;
});
const helpChoice = (): void => {
    menuStore.setHelpChoice(true);
};
const goBack = (): void => {
    menuStore.resetChoices();
};
</script>
