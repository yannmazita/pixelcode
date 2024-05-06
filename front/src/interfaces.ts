export interface TokenData {
    access_token: string | null,
    token_type: string | null,
}

export interface UserCreate {
    username: string,
    password: string,
}

export interface User {
    id: string,
    username: string,
    roles: string,
}

export interface EmployeeIdentifier {
    internal_id: string | null,
    email: string | null,
}

// not defined in API
export interface IdentifierStatus {
    email_exists: boolean | null,
    internal_id_exists: boolean | null,
}

export interface EmployeeState {
    internal_id: string | null,
    code_to_print: string | null,
    email_code_sent: boolean | null,
    email_code_validated: boolean | null,
}

