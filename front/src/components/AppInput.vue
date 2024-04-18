<template>
    <label v-if="label" class="label-text">{{ label }}</label>
    <input v-model="model" v-bind="{ ...$attrs, ...classes }" />
</template>
<script setup lang="ts">
import { computed } from 'vue';

interface Props {
    label?: string | boolean;
    class?: string | boolean;
}

const model = defineModel();
const props = defineProps<Props>();

const classes = computed(() => {
    if (props.class) {
        return { class: props.class };
    }
    else {
        return { class: 'input input-bordered text-xl' };
    }
})
</script>
