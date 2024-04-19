import { defineStore } from 'pinia';
import { useClientStore } from '@/stores/client.ts';
import { reactive, ref, Ref } from 'vue';
import { EmployeeStatus } from '@/interfaces.ts';

export const usePixelStore = defineStore('pixel', () => {
    const clientStore = useClientStore();
    const employeeStatus: EmployeeStatus = reactive({
        email_exists: null,
        employee_id_exists: null,
        email_code_sent: false,
        email_code_validated: false,
    });

    async function sendEmployeeInformation(employeeEmail: string, employeeId: string): Promise<void> {
        try {
            await clientStore.connectSocket();
            await clientStore.sendSocketMessage(JSON.stringify({
                action: 'employee_info',
                data: {
                    employee_id: employeeId,
                    employee_email: employeeEmail,
                },
            }));
        }
        catch (error) {
            console.log(error);
        }
    }

    async function sendEmailVerificationCode(code: number): Promise<void> {
        try {
            await clientStore.sendSocketMessage(JSON.stringify({
                action: 'email_verification',
                data: {
                    email_code: code,
                },
            }));
        }
        catch (error) {
            console.log(error);
        }
    }

    return {
        employeeStatus,
        sendEmployeeInformation,
        sendEmailVerificationCode,
    }
})
