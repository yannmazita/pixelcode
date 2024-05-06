import { reactive, computed } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';
import { useSettingsStore } from '@/stores/settings.ts';
import { EmployeeIdentifier, EmployeeState, IdentifierStatus } from '@/interfaces.ts';

export const usePixelStore = defineStore('pixel', () => {
    const settingsStore = useSettingsStore();
    const kioskMode = computed(() => settingsStore.screenWidth > import.meta.env.VITE_KIOSK_WIDTH_CUTOFF)
    const identifierStatus: IdentifierStatus = reactive({
        email_exists: null,
        internal_id_exists: null,
    });
    const employeeState: EmployeeState = reactive({
        internal_id: null,
        code_to_print: null,
        email_code_sent: null,
        email_code_validated: null,
    });

    async function sendEmployeeIdentifier(identity: EmployeeIdentifier): Promise<void> {
        try {
            const response = await axios.post(
                `${import.meta.env.VITE_API_URL}/employees/send-email/`,
                identity,
                {
                    headers: {
                        accept: 'application/json',
                    }
                }
            );
            //Object.assign(employeeState, response.data);
            employeeState.email_code_sent = response.data.email_code_sent;
            if (identity.email) {
                identifierStatus.email_exists = true;
            }
            else if (identity.internal_id) {
                identifierStatus.internal_id_exists = true;
            }
        }
        catch (error) {
            if (identity.email) {
                identifierStatus.email_exists = false;
            }
            else if (identity.internal_id) {
                identifierStatus.internal_id_exists = false;
            }
            console.log(error);
        }
    }

    async function sendVerificationCode(identity: EmployeeIdentifier, code: number): Promise<void> {
        try {
            const response = await axios.post(
                `${import.meta.env.VITE_API_URL}/employees/verify-email/`,
                {
                    ...identity,
                    code: code,
                },
                {
                    headers: {
                        accept: 'application/json',
                    }
                }
            );
            //Object.assign(employeeState, response.data);
            employeeState.email_code_validated = response.data.email_code_validated;
        }
        catch (error) {
            console.log(error);
        }
    }

    function resetEmployeeState(): void {
        identifierStatus.email_exists = null;
        identifierStatus.internal_id_exists = null;
        employeeState.email_code_sent = null;
        employeeState.email_code_validated = null;
    }

    return {
        identifierStatus,
        employeeState,
        sendEmployeeIdentifier,
        sendVerificationCode,
        resetEmployeeState,
        kioskMode,
    }
})
