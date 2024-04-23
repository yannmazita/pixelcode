<template>
    <AppModal @click-event="() => { jumpToHome(); }" :show-modal="showModal">
        <template #headerText>{{ headerText }}</template>
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
const headerText: Ref<string> = ref<string>("");
const message: Ref<string> = ref<string>("");

const jumpToHome = (): void => {
    showModal.value = false;
    menuStore.resetChoices();
};

const identityError = computed(() => {
    if (employeeState.value.internal_id_exists === false || employeeState.value.email_exists === false) {
        return true;
    }
    else {
        return false;
    }
});
const emailCodeSent = computed(() => {
    return employeeState.value.email_code_sent;
});

watch(identityError, (newValue) => {
    headerText.value = "Incorrect identifier";
    if (newValue) {
        if (employeeState.value.internal_id_exists === false) {
            message.value = "The id you entered does not exist in the system.";
            showModal.value = true;
        }
        else if (employeeState.value.email_exists === false) {
            message.value = "The email you entered does not exist in the system.";
            showModal.value = true;
        }
    }
});
watch(emailCodeSent, (newValue) => {
    headerText.value = "Verification code";
    if (newValue) {
        message.value = "A verification code has been sent to your email.";
        showModal.value = true;
    }
    else {
        message.value = "An error occurred while sending the verification code.";
        showModal.value = true;
    }
});
</script>
