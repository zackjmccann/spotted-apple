
export type CreateAccountState = {
    created: boolean;
    errors?: Record<string, string[]>;
    formData?: Record<string, string>;
}

export type CreateAccountFormProps = {
    state: CreateAccountState,
    formAction: string | ((formData: FormData) => void | Promise<void>) | undefined;
}
