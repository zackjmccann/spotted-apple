'use client';

import { loginUser, LoginState } from '@/app/lib/actions';
import { useActionState } from 'react';
import { useFormStatus, useFormState } from 'react-dom'

export default function LoginForm() {
    const initialState: LoginState = { message: null, errors: {} };
    const [state, formAction] = useFormState(loginUser, initialState);
  
    return (
        <form action={formAction}>
            <label htmlFor='email' className='mb-2 block text-sm font-medium'>
                Email
            </label>
            <input
                name='email'
                type='string'
                placeholder='example@email.com'
            />
            <label htmlFor='password' className='mb-2 block text-sm font-medium'>
                Password
            </label>
            <input
                name='password'
                type='string'
            />
            <SubmitButton />
        </form>
    )
};

function SubmitButton() {
    const { pending } = useFormStatus()
  
    return (
      <button type="submit" disabled={pending}>
        {pending ? 'logging in...' : 'Login'}
      </button>
    )
};