export type AccountData = {
  email: string,
  firstName: string,
  lastName: string
}

export type SignUpState = {
    created: boolean;
    passwordSet: boolean;
    errors?: Record<string, string[]>;
    formData?: Record<string, string>;
    accountData?: AccountData;
  }

export type FormAction = (payload: FormData) => void;

export type SignUpProps = {
  state: SignUpState;
  action: FormAction;
}

