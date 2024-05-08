<template>
    <dialog class="modal" :class="{ 'modal-open': props.showModal }">
        <div id="user-edit-form-container" class="modal-box">
            <form @submit="onSubmit" method="post">
                <div class="flex flex-col">
                    <AppInput v-model="username" :label="'Username'"></AppInput>
                    <AppInput v-model="roles" :label="'Roles'"></AppInput>
                    <div id="user-edit-form-buttons">
                        <button :disabled="isSubmitting" type="submit" class="btn btn-primary">Save</button>
                        <button @click="closeModal()" type="button" class="btn btn-primary">Cancel</button>
                    </div>
                </div>
            </form>
        </div>
    </dialog>
</template>
<script setup lang="ts">
import { watch } from 'vue';
import { useForm } from 'vee-validate';
import { toTypedSchema } from '@vee-validate/yup';
import { object, string } from 'yup';
import { useUserStore } from '@/stores/user.ts';
import AppInput from '@/components/AppInput.vue';

interface Props {
    showModal: boolean;
    userId: string | null;
}
const props = defineProps<Props>();
const emit = defineEmits<{
    'closeEvent': [value: boolean],
    'updateEvent': [value: boolean],
}>();
const userStore = useUserStore();

const closeModal = () => {
    emit('closeEvent', false);
};
const notifyUpdate = () => {
    emit('updateEvent', true);
};

const schema = toTypedSchema(
    object({
        username: string().required().min(1).max(255),
        roles: string().required().min(1).max(255),
    }),
);
const { handleSubmit, isSubmitting, defineField } = useForm({
    validationSchema: schema,
});
const [username] = defineField('username');
const [roles] = defineField('roles');
const onSubmit = handleSubmit(async (values, { resetForm }) => {
    if (props.userId) {
        await userStore.updateUserUsername(props.userId, values.username);
        await userStore.updateUserRoles(props.userId, values.roles);
    }
    resetForm();
    notifyUpdate();
    closeModal();
});

watch(() => props.userId, (newUserId) => {
    if (newUserId) {
        const user = userStore.users.find((user) => user.id === newUserId);
        if (user) {
            username.value = user.username;
            roles.value = user.roles;
        }
    }
});
</script>
