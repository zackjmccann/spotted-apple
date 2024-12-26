export type TestFormState = {
    formData?: Record<string, string>;
}

export type TestFormProps = {
    state: TestFormState,
    formAction: string | ((formData: FormData) => void | Promise<void>) | undefined;
}