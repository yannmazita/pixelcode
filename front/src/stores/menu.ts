import { defineStore } from 'pinia';
import { ref, Ref } from 'vue';

export const useMenuStore = defineStore('menu', () => {
    const informationChoice: Ref<boolean> = ref(false); // The user has chosen to input employee information.
    const codeChoice: Ref<boolean> = ref(false); // The user has chosen to input code received by email.
    const helpChoice: Ref<boolean> = ref(false); // The user has chosen to go to the help page.
    const currentPageTitle: Ref<string> = ref("Home"); // The title of the current page.
    const informationType: Ref<string | null> = ref(null); // The type of information the user is inputting.

    function setInformationTypeEmail(): void {
        informationType.value = "email";
    }
    function setInformationTypeID(): void {
        informationType.value = "id";
    }

    function setInformationChoice(value: boolean): void {
        informationChoice.value = value;
        codeChoice.value = !value;
        helpChoice.value = !value;
        currentPageTitle.value = "Employee Information";
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



    return {
        informationType,
        informationChoice,
        codeChoice,
        helpChoice,
        setInformationChoice,
        currentPageTitle,
        setCodeChoice,
        setHelpChoice,
        setInformationTypeID,
        setInformationTypeEmail,
        resetChoices,
    }
})

