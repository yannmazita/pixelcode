export interface TokenData {
    access_token: string | null,
    token_type: string | null,
}

export interface User {
    id: string | null,
    username: string | null,
}

export interface EmployeeIdentifier {
    internal_id: string | null,
    email: string | null,
}

export interface EmployeeState {
    email_exists: boolean | null,
    internal_id_exists: boolean | null,
    email_code_sent: boolean,
    email_code_validated: boolean,
}

