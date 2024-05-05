<template>
    <div id="app-user-list-container" class="flex justify-center">
        <table id="app-user-list-table" class="border-collapse shadow-md">
            <thead>
                <tr class="bg-gray-100">
                    <th class="p-2 border">ID</th>
                    <th class="p-2 border">Username</th>
                    <th class="p-2 border">Roles</th>
                    <th class="p-2 border">Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in userStore.users" :key="user.id">
                    <td class="p-2 border">
                        <div class="flex justify-center">
                            <div class="tooltip" v-bind:data-tip="user.id">
                                {{ truncateData(user.id) }}
                            </div>
                        </div>
                    </td>
                    <td class="p-2 border">
                        <div class="flex justify-center">
                            <div class="tooltip" v-bind:data-tip="user.username">
                                {{ truncateData(user.username) }}
                            </div>
                        </div>
                    </td>
                    <td class="p-2 border">
                        <div class="flex justify-center">
                            <div class="tooltip" v-bind:data-tip="user.roles">
                                {{ truncateData(user.roles) }}
                            </div>
                        </div>
                    </td>
                    <td class="p-2 border">
                        <div class="flex justify-center">
                            <button @click="editUser(user.id)">📝</button>
                            <button @click="deleteUser(user.id)">❌</button>
                        </div>
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

const truncateData = (data: string) => {
    if (data.length > 8) {
        return data.substring(0, 8) + '...';
    }
    else {
        return data;
    }
};

const editUser = (id: string) => {
    console.log('Edit user:', id);
};

const deleteUser = (id: string) => {
    //userStore.deleteUser(id);
    console.log('Delete user:', id);
};
</script>
