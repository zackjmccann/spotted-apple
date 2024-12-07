'use client';

import { useActionState } from 'react'
import { SignUpState, SignUpProps, FormAction} from '@/app/features/sign-up-feature/types'
import { createAccount } from '@/app/features/create-account-form-feature/actions';
import { setPassword } from '@/app/features/create-set-password-form-feature/actions';

export default function signUp(state: SignUpState): SignUpProps {
    let formState: SignUpState;
    let formAction: FormAction;

    if (!state.created) {
        [formState, formAction] = useActionState(createAccount, state);
    } else {
        [formState, formAction] = useActionState(setPassword, state);
    }

    return {state: formState, formAction: formAction}
};
