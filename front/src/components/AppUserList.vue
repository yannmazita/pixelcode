<template>
    <EditForm :show-modal="showEditForm" :user-id="editUserId" @close-event="closeEditForm"></EditForm>
    <div class="flex flex-col h-full justify-between">
        <div id="app-user-list-container" class="flex justify-center">
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
                                <button @click="openEditForm(user.id)">📝</button>
                                <button @click="">❌</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <PaginationBar @previousButtonClick="getPreviousUsers" @nextButtonClick="getNextUsers"
            :previousButtonDisabled="!canGoPrevious" :nextButtonDisabled="!canGoNext"></PaginationBar>
    </div>
</template>

<script setup lang="ts">
import { ref, Ref, onMounted, computed } from 'vue';
import { storeToRefs } from 'pinia';
import { useUserStore } from '@/stores/user.ts';
import PaginationBar from '@/components/AppPaginationBar.vue';
import EditForm from '@/components/AppUserEditForm.vue';

const userStore = useUserStore();
const currentPage: Ref<number> = ref(0);
const limit: number = 14;
const { totalUsers } = storeToRefs(userStore);
const showEditForm: Ref<boolean> = ref(false);
const editUserId: Ref<string | null> = ref(null);

onMounted(() => {
    userStore.getUsers(currentPage.value * limit, limit);
});

const canGoPrevious = computed(() => {
    return currentPage.value > 0;
});
const canGoNext = computed(() => {
    return (currentPage.value + 1) * limit < totalUsers.value
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

const openEditForm = (id: string) => {
    showEditForm.value = true;
    editUserId.value = id;
};
const closeEditForm = () => {
    showEditForm.value = false;
    editUserId.value = null;
};
</script>
