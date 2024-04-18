<template>
    <button class="btn btn-primary text-6xl active:bg-transparent h-fit w-fit py-3" @click="handleClick">
        <slot></slot>
    </button>
</template>
<script setup lang="ts">
const emit = defineEmits(['click']);

function handleClick() {
    emit('click')
}
</script>
