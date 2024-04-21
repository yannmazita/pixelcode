import { defineStore } from 'pinia';
import { ref, Ref } from 'vue';

export const useMenuStore = defineStore('menu', () => {
    const informationChoice: Ref<boolean> = ref(false); // The user has chosen to input employee information.
    const codeChoice: Ref<boolean> = ref(false); // The user has chosen to input code received by email.
    const helpChoice: Ref<boolean> = ref(false); // The user has chosen to go to the help page.
    const currentPageTitle: Ref<string> = ref("Home"); // The title of the current page.
    const identifierIdChoice: Ref<boolean> = ref(false); // The user has chosen to input their internal ID.
    const identifierEmailChoice: Ref<boolean> = ref(false); // The user has chosen to input their email.

    function setIdentifierTypeID(value: boolean): void {
        identifierIdChoice.value = value;
        identifierEmailChoice.value = !value;
    }
    function setIdentifierTypeEmail(value: boolean): void {
        identifierIdChoice.value = !value;
        identifierEmailChoice.value = value;
    }

    function setInformationChoice(value: boolean): void {
        informationChoice.value = value;
        codeChoice.value = !value;
        helpChoice.value = !value;
        currentPageTitle.value = "Find employee";
    }

    function setCodeChoice(value: boolean): void {
        informationChoice.value = !value;
        codeChoice.value = value;
        helpChoice.value = !value;
        currentPageTitle.value = "Verification code";
    }

    function setHelpChoice(value: boolean): void {
        informationChoice.value = !value;
        codeChoice.value = !value;
        helpChoice.value = value;
        currentPageTitle.value = "Help";
    }

    function resetChoices(): void {
        informationChoice.value = false;
        codeChoice.value = false;
        helpChoice.value = false;
        currentPageTitle.value = "Home";
    }

    function resetIdentifierChoices(): void {
        identifierIdChoice.value = false;
        identifierEmailChoice.value = false;
    }

    return {
        informationChoice,
        codeChoice,
        helpChoice,
        setInformationChoice,
        identifierIdChoice,
        identifierEmailChoice,
        currentPageTitle,
        setCodeChoice,
        setHelpChoice,
        setIdentifierTypeID,
        setIdentifierTypeEmail,
        resetChoices,
        resetIdentifierChoices,
    }
})

