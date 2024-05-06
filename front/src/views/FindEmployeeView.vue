<template>
    <FeedBack></FeedBack>
    <Identifier></Identifier>
    <PixelUserInput></PixelUserInput>
</template>
<script setup lang="ts">
import { onMounted } from 'vue';
import { useMenuStore } from '@/stores/menu.ts';
import { PageType } from '@/enums.ts';
import PixelUserInput from '@/components/PixelUserInput.vue'
import Identifier from '@/components/PixelIdentifierType.vue'
import FeedBack from '@/components/PixelIdentifierFeedback.vue';

const menuStore = useMenuStore();

onMounted(() => {
    menuStore.setCurrentPage(PageType.FIND_EMPLOYEE);
});
</script>
