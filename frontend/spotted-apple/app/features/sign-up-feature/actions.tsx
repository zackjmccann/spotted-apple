'use client';

import { useActionState } from 'react'
import { createAccount } from '@/app/features/create-account-form-feature/actions';
import { setPassword } from '@/app/features/create-set-password-form-feature/actions';
import { SignUpState} from '@/app/features/sign-up-feature/types'

export default function signUp(state: SignUpState) {
    if (!state.created) {
        return useActionState(createAccount, state);
    }
    
    if (state.passwordSet) {
        return useActionState(setPassword, state);
    }
};