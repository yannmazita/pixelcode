<template>
    <div id="pixel-user-input-container" class="flex justify-center">
        <form @submit="onSubmit" method="post">
            <div class="flex justify-center">
                <AppInput class="input input-bordered text-5xl w-full" v-model="userInput"></AppInput>
                <div class="text-4xl">❌</div>
            </div>
            <div class="flex justify-center">
                <Keyboard @keyPress="(key) => { updateAppInput(key); }" :keyboardKeys="keys" :additionalRows="otherRows"></Keyboard>
            </div>
            <div class="flex justify-center">
                <AppButton :disabled="isSubmitting" type="submit" class="btn btn-primary">{{ 'Submit' }}</AppButton>
            </div>
        </form>
    </div>
</template>
<script setup lang="ts">
import { useClientStore } from '@/stores/client.ts';
import { useMenuStore } from '@/stores/menu.ts';
import { computed } from 'vue';
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import { object, string } from 'yup';
import AppInput from '@/components/AppInput.vue'
import AppButton from '@/components/AppButton.vue'
import Keyboard from '@/components/AppVisualKeyboard.vue'

const clientStore = useClientStore();
const menuStore = useMenuStore();

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
    const message = JSON.stringify({
        action: 'yet_to_be_defined',
        data: {
            letter: values.userInput.toLowerCase(),
        },
    });
    clientStore.sendSocketMessage(message);
    resetForm();
});

const updateAppInput = (key: string) => {
    userInput.value = userInput.value + key;
};

const keys = computed(() => {
    if (menuStore.codeChoice) {
        return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    }
    else if (menuStore.informationChoice) {
        return;
    };
});
const otherRows = computed(() => {
    if (menuStore.codeChoice) {
        return [];
    }
    else if (menuStore.informationChoice) {
        return;
    }
});
</script>
