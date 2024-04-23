import { defineStore } from 'pinia';
import { reactive } from 'vue';
import axios from 'axios';
import { EmployeeIdentifier, EmployeeState } from '@/interfaces.ts';

export const usePixelStore = defineStore('pixel', () => {
    const employeeState: EmployeeState = reactive({
        email_exists: null,
        internal_id_exists: null,
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
                employeeState.email_exists = true;
            }
            else if (identity.internal_id) {
                employeeState.internal_id_exists = true;
            }
        }
        catch (error) {
            if (identity.email) {
                employeeState.email_exists = false;
            }
            else if (identity.internal_id) {
                employeeState.internal_id_exists = false;
            }
            console.log(error);
        }
    }

    async function sendEmailVerificationCode(identity: EmployeeIdentifier, code: number): Promise<void> {
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
        employeeState.email_exists = null;
        employeeState.internal_id_exists = null;
        employeeState.email_code_sent = null;
        employeeState.email_code_validated = null;
    }

    return {
        employeeState,
        sendEmployeeIdentifier,
        sendEmailVerificationCode,
        resetEmployeeState,
    }
})
