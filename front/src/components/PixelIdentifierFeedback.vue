<template>
    <AppModal @click-event="() => { jumpToHome }" :show-modal="showModal">
        <template #headerText>Incorrect identifier</template>
        <template #paragraphText>{{ message }}</template>
        <template #buttonText>Close</template>
    </AppModal>
</template>
<script setup lang="ts">
import { computed, watch, ref, Ref } from 'vue';
import { storeToRefs } from 'pinia';
import { usePixelStore } from '@/stores/pixel.ts';
import { useMenuStore } from '@/stores/menu.ts';
import AppModal from '@/components/AppModalOneButton.vue';

const pixelStore = usePixelStore();
const menuStore = useMenuStore();
const { employeeState } = storeToRefs(pixelStore);
const showModal: Ref<boolean> = ref<boolean>(false);
const message: Ref<string> = ref<string>("");

const jumpToHome = (): void => {
    showModal.value = false;
    menuStore.resetChoices();
};

const identified = computed(() => {
    if (employeeState.value.internal_id_exists === true || employeeState.value.email_exists === true) {
        return true;
    }
    else {
        return false;
    }
});

watch(identified, (newValue) => {
    if (!newValue) {
        showModal.value = true;
        if (employeeState.value.internal_id_exists === false) {
            message.value = "The id you entered does not exist in the system.";
        }
        else if (employeeState.value.email_exists === false) {
            message.value = "The email you entered does not exist in the system.";
        }
    }
});
</script>
