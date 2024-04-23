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

// The api will send internal_id on successful employee retrieval instead of email_exists/internal_id_exists
export interface EmployeeState {
    email_exists: boolean | null,   // not defined in API
    internal_id_exists: boolean | null, // not defined in API
    code_to_print: string | null,
    email_code_sent: boolean | null,
    email_code_validated: boolean | null,
}

