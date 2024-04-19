export interface TokenData {
    access_token: string | null,
    token_type: string | null,
}

export interface User {
    id: string | null,
    username: string | null,
}

export interface ServerStats {
    active_users: number,
}

export interface Employee {
    id: string | null,
    employee_id: string | null,
    email: string | null,
}

export interface EmployeeStatus {
    email_exists: boolean | null,
    employee_id_exists: boolean | null,
    email_code_sent: boolean,
    email_code_validated: boolean,
}
