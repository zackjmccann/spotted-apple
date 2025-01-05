import { FormAction } from '@/lib/forms/types'
  
export type LoginState = {
    errors?: Record<string, string[]>;
    formData?: Record<string, string>;
}

export type LoginProps = {
    state: LoginState;
    action: FormAction;
}

export type AccessTokens = {
    idToken: string,
    accessToken: string,
    refreshToken: string,
}
