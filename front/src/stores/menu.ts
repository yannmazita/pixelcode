import { defineStore } from 'pinia';
import { ref, Ref } from 'vue';

export const useMenuStore = defineStore('menu', () => {
    const findEmployeeChoice: Ref<boolean> = ref(false); // The user has chosen to find an employee 
    const codeChoice: Ref<boolean> = ref(false); // The user has chosen to input code received by email.
    const helpChoice: Ref<boolean> = ref(false); // The user has chosen to go to the help page.
    const adminChoice: Ref<boolean> = ref(false); // The user has chosen to go to the admin page.
    const currentPageTitle: Ref<string> = ref("Home"); // The title of the current page.
    const findEmployeeByInternalIDChoice: Ref<boolean> = ref(false); // The user has chosen to find employee by internal ID.
    const findEmployeeByEmailChoice: Ref<boolean> = ref(false); // The user has chosen to find employee by email.

    function setIdentifierTypeID(value: boolean): void {
        findEmployeeByInternalIDChoice.value = value;
        findEmployeeByEmailChoice.value = !value;
    }
    function setIdentifierTypeEmail(value: boolean): void {
        findEmployeeByInternalIDChoice.value = !value;
        findEmployeeByEmailChoice.value = value;
    }

    function setFindEmployeeChoice(value: boolean): void {
        findEmployeeChoice.value = value;
        codeChoice.value = !value;
        helpChoice.value = !value;
        adminChoice.value = !value;
        currentPageTitle.value = "Find employee";
    }

    function setCodeChoice(value: boolean): void {
        findEmployeeChoice.value = !value;
        codeChoice.value = value;
        helpChoice.value = !value;
        adminChoice.value = !value;
        currentPageTitle.value = "Verification code";
    }

    function setHelpChoice(value: boolean): void {
        findEmployeeChoice.value = !value;
        codeChoice.value = !value;
        helpChoice.value = value;
        adminChoice.value = !value;
        currentPageTitle.value = "Help";
    }
    function setAdminChoice(value: boolean): void {
        findEmployeeChoice.value = !value;
        codeChoice.value = !value;
        helpChoice.value = !value;
        adminChoice.value = value;
        currentPageTitle.value = "Admin";
    }

    function resetChoices(): void {
        findEmployeeChoice.value = false;
        codeChoice.value = false;
        helpChoice.value = false;
        adminChoice.value = false;
        currentPageTitle.value = "Home";
    }

    function resetIdentifierChoices(): void {
        findEmployeeByInternalIDChoice.value = false;
        findEmployeeByEmailChoice.value = false;
    }

    return {
        findEmployeeChoice,
        codeChoice,
        helpChoice,
        adminChoice,
        findEmployeeByInternalIDChoice,
        findEmployeeByEmailChoice,
        currentPageTitle,
        setFindEmployeeChoice,
        setCodeChoice,
        setHelpChoice,
        setAdminChoice,
        setIdentifierTypeID,
        setIdentifierTypeEmail,
        resetChoices,
        resetIdentifierChoices,
    }
})

