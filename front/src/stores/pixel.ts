import { defineStore } from 'pinia';
import { reactive, ref, Ref } from 'vue';
import axios from 'axios';
import { EmployeeIdentifier, EmployeeState } from '@/interfaces.ts';

export const usePixelStore = defineStore('pixel', () => {
    const employeeState: EmployeeState = reactive({
        email_exists: null,
        internal_id_exists: null,
        email_code_sent: false,
        email_code_validated: false,
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
            Object.assign(employeeState, response.data);
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
            Object.assign(employeeState, response.data);
        }
        catch (error) {
            console.log(error);
        }
    }

    return {
        employeeState,
        sendEmployeeIdentifier,
        sendEmailVerificationCode,
    }
})
