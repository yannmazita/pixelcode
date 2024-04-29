<template>
    <div class="user-management">
        <h2 class="text-2xl">Manage Users</h2>
        <form @submit="onSubmit" method="post" class="card-body bg-base-200">
            <div class="form-control">
                <AppInput v-model="username" class="input input-bordered" :label="'Username'"></AppInput>
            </div>
            <div class="form-control">
                <AppInput v-model="password" class="input input-bordered" :label="'Password'" type="password">
                </AppInput>
            </div>
            <div class="form-control mt-6">
                <AppButton :disabled="isSubmitting" type="submit" class="btn btn-primary text-sm">
                    {{ 'Submit' }}
                </AppButton>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import { object, string } from 'yup';
import { useAuthenticationStore } from '@/stores/authentication.ts';
import AppInput from '@/components/AppInput.vue';
import AppButton from '@/components/AppButton.vue';

const authenticationStore = useAuthenticationStore();
const tokenData = authenticationStore.tokenData;
const isEdit = ref(false);
const form = reactive({
    username: '',
    password: '',
});

const schema = toTypedSchema(
    object({
        username: string().required().min(1).max(255).default(''),
        password: string().required().min(1).max(255).default(''),
    }),
);
const { handleSubmit, isSubmitting, defineField } = useForm({
    validationSchema: schema,
});

const [username] = defineField('username');
const [password] = defineField('password');

const onSubmit = handleSubmit(async (values, { resetForm }) => {
});
</script>
