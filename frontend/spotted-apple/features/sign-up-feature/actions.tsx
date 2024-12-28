import { SignUpState} from '@/features/sign-up-feature/types'
import { createAccount } from '@/features/create-account-form-feature/actions';
import { setPassword } from '@/features/create-set-password-form-feature/actions';

export default function signUp(prevState: SignUpState, formData: FormData) {
    console.log('Sign Up...')
    if (!prevState.created) {
        return createAccount(prevState, formData)
    } else {
        return setPassword(prevState, formData)
    }
};
