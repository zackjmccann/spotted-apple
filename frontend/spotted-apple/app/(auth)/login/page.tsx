'use client';

import { useActionState } from 'react'
import { Banner } from '@/features/banner-feature'
import { LoginProps, LoginState } from '@/features/login/types'
import { login } from '@/features/login/actions'
import LoginForm from '@/features/login/form'


export default function Page() {
  const initialLoginState: LoginState = {};
  const [state, formAction] = useActionState(login, initialLoginState)
  const loginProps: LoginProps = {state: state, action: formAction}

  return (
    <main className="flex min-h-screen flex-row items-center justify-around p-12">
        <Banner />
        <LoginForm {...loginProps}/>
    </main>
  );
};
