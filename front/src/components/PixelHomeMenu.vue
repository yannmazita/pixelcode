<template>
    <menu id="pixel-home-menu-container">
        <div id="pixel-home-menu" class="grid grid-flow-row">
            <li id="pixel-home-menu-information-choice" class="flex justify-center m-5">
                <AppButton @click="informationChoice" class="">{{ 'Find employee' }}</AppButton>
            </li>
            <li id="pixel-home-menu-code-choice" class="flex justify-center m-5">
                <AppButton @click="codeChoide">{{ 'Verification code' }}</AppButton>
            </li>
        </div>
    </menu>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useMenuStore } from '@/stores/menu.ts'
import { usePixelStore } from '@/stores/pixel.ts'
import AppButton from '@/components/AppButton.vue';

const menuStore = useMenuStore();
const pixelStore = usePixelStore();

const informationChoice = (): void => {
    menuStore.setInformationChoice(true);
}
const codeChoide = (): void => {
    menuStore.setCodeChoice(true);
}

onMounted(() => {
    menuStore.resetChoices();
    pixelStore.resetEmployeeState();
});
</script>
