export interface TokenData {
    access_token: string | null,
    token_type: string | null,
}

export interface ServerStats {
    active_users: number,
}

export interface EmployeeStatus {
    email_exists: boolean | null,
    employee_id_exists: boolean | null,
    email_code_sent: boolean,
    email_code_validated: boolean,
}

