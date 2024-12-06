
export type SetPasswordState = {
    passwordSet: boolean;
    errors?: Record<string, string[]>;
    formData?: Record<string, string | File>;
}
