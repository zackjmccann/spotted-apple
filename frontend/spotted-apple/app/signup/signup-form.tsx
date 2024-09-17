'use client';

import { createUser, CreateState } from '@/app/lib/actions';
import { useActionState } from 'react';
import { useFormStatus, useFormState } from 'react-dom'
import styles from '@/app/ui/styles.module.css'

export default function CreateForm() {
    const initialState: CreateState = { message: null, errors: {} };
    const [state, formAction] = useFormState(createUser, initialState);
  
    return (
            <form className={styles.form} action={formAction}>
                <input
                    name='firstName'
                    type='string'
                    placeholder='First Name'
                />
                <input
                    name='lastName'
                    type='string'
                    placeholder='Last Name'
                />
                <input
                    name='phoneNumber'
                    type='string'
                    placeholder='Phone Number'
                />
                <input
                    name='email'
                    type='string'
                    placeholder='Email'
                />
                <input
                    name='password'
                    type='string'
                    placeholder='Password'
                />
                <input
                    name='confirmPassword'
                    type='string'
                    placeholder='Confirm Password'
                />
                <SubmitButton />
                <p className='text-sky-700 text-xs'>Already have an account? Sign in</p>
            </form>
    )
};

function SubmitButton() {
    const { pending } = useFormStatus()
  
    return (
      <button className='w-full h-10 font-semibold rounded-lg bg-[#0141ff]' type="submit" disabled={pending}>
        {pending ? 'creating account...' : 'Create Account'}
      </button>
    )
};