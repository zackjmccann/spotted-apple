'use client';

import { loginUser, LoginState } from '@/app/lib/actions';
import { useActionState } from 'react';
import { useFormStatus, useFormState } from 'react-dom'
import styles from '@/app/ui/styles.module.css'

export default function LoginForm() {
    const initialState: LoginState = { message: null, errors: {} };
    const [state, formAction] = useFormState(loginUser, initialState);
  
    return (
            <form className={styles.form} action={formAction}>
                <input
                    name='email'
                    type='string'
                    placeholder='Email, username, phone number'
                />
                <input
                    name='password'
                    type='string'
                    placeholder='Password'
                />
                <SubmitButton />
            </form>
    )
};

function SubmitButton() {
    const { pending } = useFormStatus()
  
    return (
      <button className='w-full h-10 font-semibold rounded-lg bg-[#0141ff]' type="submit" disabled={pending}>
        {pending ? 'logging in...' : 'Log In'}
      </button>
    )
};