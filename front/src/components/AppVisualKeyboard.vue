<template>
    <div id="app-visual-keyboard-container" class="py-8 w-fit">
        <div :id="`app-visual-keyboard-row-container-${index}`" v-for="(row, index) in keyboardRows" :key="index">
            <div :id="`app-visual-keyboard-row-${index}`" class="flex justify-center">
                <button :id="`app-visual-keyboard-key-${key}`" v-for="key in row" :key="key"
                    @click="emit('keyPress', key)" class="kbd text-white text-4xl bg-blue-600 m-1" type="button">
                    {{ key }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
    additionalRows?: string[][];
    keyboardKeys?: string[];
    hiddenKeys?: string[];
}

const props = withDefaults(defineProps<Props>(), {
    hiddenKeys: () => [],
    keyboardKeys: () => [
        'A', 'Z', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'Q', 'S', 'D',
        'F', 'G', 'H', 'J', 'K', 'L', 'M', '', '', 'W', 'X', 'C', 'V', 'B', 'N', '', '⬅️'
    ],
    additionalRows: () => [
        ['-', '_', '.', '@'],
        ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    ],
});
const emit = defineEmits<{
    keyPress: [key: string]
}>();

const keyboardRows = computed(() => {
    const visibleKeys = props.keyboardKeys.filter(key => !props.hiddenKeys.includes(key));
    const rows = props.additionalRows;
    for (let i = 0; i < Math.ceil(visibleKeys.length / 10); i++) {
        rows.push(visibleKeys.slice(i * 10, (i + 1) * 10));
    }
    return rows;
});
</script>
