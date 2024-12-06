
export type CreateAccountState = {
    created: boolean;
    errors?: Record<string, string[]>;
    formData?: Record<string, string>;
}
