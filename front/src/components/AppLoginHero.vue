<template>
    <div class="hero min-h-screen">
        <div class="hero-content flex-col lg:flex-row-reverse">
            <div class="text-center lg:text-left">
                <h1 class="text-5xl font-bold">Login now!</h1>
                <p class="py-6">Connect to the administration dashboard.</p>
            </div>
            <div class="card shrink-0 w-full max-w-sm shadow-2xl bg-base-100">
                <form class="card-body bg-base-200">
                    <div class="form-control">
                        <AppInput v-model="username" placeholder="username" class="input input-bordered"></AppInput>
                    </div>
                    <div class="form-control">
                        <AppInput v-model="password" placeholder="password" class="input input-bordered"></AppInput>
                    </div>
                    <div class="form-control mt-6">
                        <AppButton :disabled="isSubmitting" type="submit" class="btn btn-primary text-sm">
                            {{ 'Submit' }}
                        </AppButton>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import { object, string } from 'yup';
import AppInput from '@/components/AppInput.vue'
import AppButton from '@/components/AppButton.vue'

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
</script>
