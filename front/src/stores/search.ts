import { defineStore } from 'pinia';
import { ref, Ref } from 'vue';
import { SearchType } from '@/enums.ts';

export const useSearchStore = defineStore('search', () => {
    const currentType: Ref<SearchType> = ref(SearchType.NONE);

    function setSearchById() {
        currentType.value = SearchType.SEARCH_BY_ID;
    }

    function setSearchByEmail() {
        currentType.value = SearchType.SEARCH_BY_EMAIL;
    }

    function clearSearch() {
        currentType.value = SearchType.NONE;
    }

    return {
        currentType,
        setSearchById,
        setSearchByEmail,
        clearSearch
    };
});
