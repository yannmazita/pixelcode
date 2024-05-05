<template>
    <div>
        <div id="app-user-list-container" class="flex flex-col h-full">
            <table id="app-user-list-table" class="w-full border-collapse shadow-md">
                <thead>
                    <tr class="bg-gray-100">
                        <th class="py-1 border">ID</th>
                        <th class="py-1 border">Username</th>
                        <th class="py-1 border">Roles</th>
                        <th class="py-1 border">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in userStore.users" :key="user.id">
                        <td class="p-1 border">
                            <div class="flex justify-center">
                                <div class="tooltip" v-bind:data-tip="user.id">
                                    {{ truncateData(user.id) }}
                                </div>
                            </div>
                        </td>
                        <td class="p-1 border">
                            <div class="flex justify-center">
                                <div class="tooltip" v-bind:data-tip="user.username">
                                    {{ truncateData(user.username) }}
                                </div>
                            </div>
                        </td>
                        <td class="p-1 border">
                            <div class="flex justify-center">
                                <div class="tooltip" v-bind:data-tip="user.roles">
                                    {{ truncateData(user.roles) }}
                                </div>
                            </div>
                        </td>
                        <td class="p-1 border">
                            <div class="flex justify-center">
                                <button @click="editUser(user.id)">📝</button>
                                <button @click="deleteUser(user.id)">❌</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <PaginationBar @previousButtonClick="getPreviousUsers" @nextButtonClick="getNextUsers"></PaginationBar>
    </div>
</template>

<script setup lang="ts">
import { ref, Ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user.ts';
import PaginationBar from '@/components/AppPaginationBar.vue';

const userStore = useUserStore();
const currentPage: Ref<number> = ref(0);
const limit: number = 14;

onMounted(() => {
    userStore.getUsers(currentPage.value * limit, limit);
});


const getPreviousUsers = () => {
    if (currentPage.value > 0) {
        currentPage.value--;
        userStore.getUsers(currentPage.value * limit, limit);
    }
};
const getNextUsers = () => {
    currentPage.value++;
    userStore.getUsers(currentPage.value * limit, limit);
};

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
