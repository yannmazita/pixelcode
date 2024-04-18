<template>
    <dialog class="modal modal-bottom" :class="{ 'modal-open': props.showModal }">
        <div class="modal-box">
            <h3 class="font-bold text-lg"><slot name="headerText"></slot></h3>
            <p class="py-4"><slot name="paragraphText"></slot></p>
            <div class="modal-action">
                <form method="dialog">
                    <button @click="emit('clickEventA', true)" class="btn mr-2"><slot name="buttonTextA"></slot></button>
                    <button @click="emit('clickEventB', true)" class="btn ml-2"><slot name="buttonTextB"></slot></button>
                </form>
            </div>
        </div>
    </dialog>
</template>
<script setup lang="ts">
interface Props {
    showModal: boolean;
}

const props = defineProps<Props>();

const emit = defineEmits<{
    'clickEventA': [value: boolean],
    'clickEventB': [value: boolean],
}>();
</script>
