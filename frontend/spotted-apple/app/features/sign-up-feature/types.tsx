export type SignUpState = {
    created: boolean;
    passwordSet: boolean;
    errors?: Record<string, string[]>;
    formData?: Record<string, string>;
  }
  
export type SignUpProps = {
  state: SignUpState;
  formAction: string | ((formData: FormData) => void | Promise<void>) | undefined;
}