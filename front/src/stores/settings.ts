import { ref, Ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useSettingsStore = defineStore('settings', () => {
    const screenWidth: Ref<number> = ref(window.innerWidth);
    const screenHeight: Ref<number> = ref(window.innerHeight);
    const darkMode: Ref<boolean> = ref(false);

    return {
        screenWidth,
        screenHeight,
        darkMode,
    }
});
