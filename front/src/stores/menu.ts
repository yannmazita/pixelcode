import { defineStore } from 'pinia';
import { ref, Ref } from 'vue';
import { PageType } from '@/enums.ts';

export const useMenuStore = defineStore('menu', () => {
    const currentPage: Ref<PageType> = ref(PageType.HOME);

    function setCurrentPage(page: PageType): void {
        currentPage.value = page;
    }

    function resetPage(): void {
        currentPage.value = PageType.HOME;
    }

    return {
        currentPage,
        setCurrentPage,
        resetPage,
    }
});
