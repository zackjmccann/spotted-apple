
export type SetPasswordState = {
    passwordSet: boolean;
    errors?: Record<string, string[]>;
    formData?: Record<string, string>;
}

export type SetPasswordFormProps = {
    state: SetPasswordState,
    formAction: string | ((formData: FormData) => void | Promise<void>) | undefined;
}
