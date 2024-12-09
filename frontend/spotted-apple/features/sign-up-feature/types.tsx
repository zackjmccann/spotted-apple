export type SignUpState = {
    created: boolean;
    passwordSet: boolean;
    errors?: Record<string, string[]>;
    formData?: Record<string, string>;
  }

export type FormAction = (payload: FormData) => void;

export type SignUpProps = {
  state: SignUpState;
  formAction: FormAction;
}