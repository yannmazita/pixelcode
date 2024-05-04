<template>
    <div id="app-user-list-container">
        <table id="app-user-list-table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Roles</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in userStore.users" :key="user.id">
                    <td>{{ user.id }}</td>
                    <td>{{ user.username }}</td>
                    <td>{{ user.roles }}</td>
                    <td>
                        <button @click="editUser(user.id)">Edit</button>
                        <button @click="deleteUser(user.id)">Delete</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useUserStore } from '@/stores/user.ts';

const userStore = useUserStore();

onMounted(() => {
    userStore.getUsers();
});

const editUser = (id: string) => {
    console.log('Edit user:', id);
};

const deleteUser = (id: string) => {
    userStore.deleteUser(id);
};
</script>
