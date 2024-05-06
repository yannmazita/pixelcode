<template>
    <div id="pixel-user-input-container" class="flex justify-center">
        <form @submit="onSubmit" method="post">
            <div class="flex justify-center">
                <AppInput class="input input-bordered text-3xl xl:text-5xl max-w-[calc(100vw-60px)]" v-model="userInput"></AppInput>
                <div v-if="showKeyboards" class="button text-4xl mx-2" @click="userInput = ''">❌</div>
            </div>
            <div class="flex justify-center">
                <Keyboard v-if="showKeyboards" @keyPress="(key) => { updateAppInput(key); }" :keyboardKeys="keys"
                    :additionalRows="otherRows">
                </Keyboard>
            </div>
            <div class="flex justify-center">
                <AppButton :disabled="isSubmitting" type="submit" class="btn btn-primary">{{ 'Submit' }}</AppButton>
            </div>
        </form>
    </div>
</template>
<script setup lang="ts">
import { useMenuStore } from '@/stores/menu.ts';
import { usePixelStore } from '@/stores/pixel.ts';
import { useSearchStore } from '@/stores/search.ts';
import { useSettingsStore } from '@/stores/settings.ts';
import { computed, onMounted, onUnmounted } from 'vue';
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import { object, string } from 'yup';
import AppInput from '@/components/AppInput.vue';
import AppButton from '@/components/AppButton.vue';
import Keyboard from '@/components/AppVisualKeyboard.vue';
import { PageType, SearchType } from '@/enums.ts';

const menuStore = useMenuStore();
const pixelStore = usePixelStore();
const searchStore = useSearchStore();
const settingsStore = useSettingsStore();

const schema = toTypedSchema(
    object({
        userInput: string().required().min(1).max(255).default(''),
    }),
);
const { handleSubmit, isSubmitting, defineField } = useForm({
    validationSchema: schema,
});
const [userInput] = defineField('userInput');

const onSubmit = handleSubmit(async (values, { resetForm }) => {
    if (searchStore.currentType === SearchType.SEARCH_BY_EMAIL) {
        await pixelStore.sendEmployeeIdentifier({
            internal_id: null,
            email: values.userInput.toLowerCase(),
        });
    } else if (searchStore.currentType === SearchType.SEARCH_BY_ID) {
        await pixelStore.sendEmployeeIdentifier({
            internal_id: values.userInput,
            email: null,
        });
    } else if (menuStore.currentPage === PageType.VERIFICATION_CODE) {
        //await pixelStore.sendVerificationCode(internal_id, values.userInput);
    }

    resetForm();
});

const updateAppInput = (key: string) => {
    if (key === '⬅️') {
        userInput.value = userInput.value?.slice(0, -1);
    }
    else {
        userInput.value = userInput.value + key;
    }
};

const keys = computed(() => {
    if (menuStore.currentPage === PageType.VERIFICATION_CODE) {
        return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    }
    else if (menuStore.currentPage === PageType.FIND_EMPLOYEE) {
        return;
    };
});
const otherRows = computed(() => {
    if (menuStore.currentPage === PageType.VERIFICATION_CODE) {
        return [];
    }
    else if (menuStore.currentPage === PageType.FIND_EMPLOYEE) {
        return;
    }
});
const showKeyboards = computed(() => {
    return pixelStore.kioskMode;
});

// Update screen size on component mount
onMounted(() => {
    window.addEventListener('resize', settingsStore.handleResize);
});
onUnmounted(() => {
    window.removeEventListener('resize', settingsStore.handleResize);
});
</script>
