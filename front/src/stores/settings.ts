import { ref, Ref } from 'vue';
import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', () => {
    const screenWidth: Ref<number> = ref(window.innerWidth);
    const screenHeight: Ref<number> = ref(window.innerHeight);

    // Handle window resize, add/remove 'resize' event listeners to this function
    const handleResize = () => {
        screenWidth.value = window.innerWidth;
        screenHeight.value = window.innerHeight;
    }
    const darkMode: Ref<boolean> = ref(false);

    return {
        screenWidth,
        screenHeight,
        handleResize,
        darkMode,
    }
});
