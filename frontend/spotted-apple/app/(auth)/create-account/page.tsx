'use client';

import { useActionState } from 'react'
import { SignUpState, SignUpProps} from '@/features/sign-up-feature/types';
import { Banner } from '@/features/banner-feature'
import signUp from '@/features/sign-up-feature/actions';
import CreateAccountForm from '@/features/create-account-form-feature/form';
import SetPasswordForm from '@/features/create-set-password-form-feature/form'


export default function Page() {
  const initialSignUpState: SignUpState = {created: false, passwordSet: false};
  const [state, formAction] = useActionState(signUp, initialSignUpState)
  const signUpProps: SignUpProps = {state: state, action: formAction}

  return (
    <main className="flex min-h-screen flex-row items-center justify-around p-12">
        <Banner />
        {!state.created ? <CreateAccountForm {...signUpProps}/> : <SetPasswordForm {...signUpProps}/>}
    </main>
  );
};
