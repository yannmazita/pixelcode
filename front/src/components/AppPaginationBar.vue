<template>
    <div id="page-navigation-buttons" class="flex justify-center">
        <button class="btn btn-ghost text-3xl" @click="emit('previousButtonClick', true)">⬅️</button>
        <button class="btn btn-ghost text-3xl" @click="emit('nextButtonClick', true)">➡️</button>
    </div>
</template>
<script setup lang="ts">
const emit = defineEmits<{
    'previousButtonClick': [value: boolean],
    'nextButtonClick': [value: boolean],
}>();
</script>
