<template>
    <div id="page-navigation-buttons" class="flex justify-center">
        <button class="btn btn-ghost text-3xl" @click="emit('previousButtonClick', true)" v-bind:disabled="props.previousButtonDisabled">⬅️</button>
        <button class="btn btn-ghost text-3xl" @click="emit('nextButtonClick', true)" v-bind:disabled="props.nextButtonDisabled">➡️</button>
    </div>
</template>
<script setup lang="ts">
interface Props {
    previousButtonDisabled?: boolean,
    nextButtonDisabled?: boolean,
}
const props = withDefaults(defineProps<Props>(), {
    previousButtonDisabled: () => false,
    nextButtonDisabled: () => false,
});

const emit = defineEmits<{
    'previousButtonClick': [value: boolean],
    'nextButtonClick': [value: boolean],
}>();
</script>
