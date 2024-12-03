'use client';

import { setPassword, SetPasswordState } from '@/app/lib/create-account/set-password-actions';
import { useFormStatus, useFormState } from 'react-dom'

export default function SetPasswordForm() {
    const initialState: SetPasswordState = { message: null, errors: {} };
    const [state, formAction] = useFormState(setPassword, initialState);

    const userEmail = 'zackjmccann@gmail.com'

    return (
        <form className='setPassword' action={formAction}>
            <input name='email' type='string' value={userEmail}/>
            <input name='password' type='password' placeholder='password' />
            <input name='confirmPassword' type='password' placeholder='confirmPassword' />
            <SubmitButton />
        </form>
    )
};

function SubmitButton() {
    const { pending } = useFormStatus()
  
    return (
      <button type="submit" disabled={pending}>
        {pending ? 'creating account...' : 'Create Account'}
      </button>
    )
};
