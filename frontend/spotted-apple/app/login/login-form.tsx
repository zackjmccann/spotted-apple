'use client';

import { useRef, useState, useEffect } from "react";
import { useFormState } from 'react-dom'

import {Icon} from 'react-icons-kit';
import {eye} from 'react-icons-kit/feather/eye';
import {eyeOff} from 'react-icons-kit/feather/eyeOff';

import { loginUser, LoginState } from '@/app/lib/login-actions';

import Link from 'next/link';
import styles from '@/app/ui/styles.module.css';

export default function LoginForm() {
    const initialState: LoginState = { message: null, errors: {} };

    const userRef = useRef<HTMLInputElement>(null);

    const [email, setEmail] = useState('')
    const [validEmail, setValidLEmail] = useState(false)

    const [password, setPassword] = useState('');
    const [validPassword, setValidPassword] = useState(false);

    const [showPassword, setShowPassword] = useState('password');
    const [icon, setIcon] = useState(eyeOff);
    
    const [state, formAction] = useFormState(loginUser, initialState);
  
    useEffect(() => {
        const emailEntry = email.length != 0; // TODO: This isn't a good check
         setValidLEmail(emailEntry);
     }, [email])
 
     useEffect(() => {
        const passwordEntry = password.length != 0;
        setValidPassword(passwordEntry);
    }, [password])

     const handleToggle = () => {
         console.log(`showPassword: ${showPassword}`)
         if (showPassword === 'password') {
             setIcon(eye);
             setShowPassword('text');
         } else {
            setIcon(eyeOff);
            setShowPassword('password');
         }
      };

    return (
            <form className={styles.form} action={formAction}>
                <label htmlFor='email' hidden>Email</label>
                <input
                    name='email'
                    id='email'
                    type='email'
                    placeholder='Email'
                    onChange={(e) => setEmail(e.target.value)}
                    value={email}
                    required
                    aria-invalid={validEmail ? 'false' : 'true'}
                    aria-describedby='emailNote'
                    />
                <label htmlFor='password' hidden>Password</label>
                <div className="mb-4 flex">
                    <input
                        name='password'
                        id='password'
                        type={showPassword}
                        placeholder='Password'
                        onChange={(e) => setPassword(e.target.value)}
                        value={password}
                        required
                        aria-invalid={validPassword ? 'false' : 'true'}
                        aria-describedby='passwordNote'
                    />
                    <span className={styles.showPassWordToggle} onClick={handleToggle}>
                        <Icon className="absolute mr-10" icon={icon}/>
                    </span>
                </div>
                <button
                    className='w-full h-10 font-semibold rounded-lg bg-[#0141ff]'
                    type="submit"
                    disabled={!validEmail || !validPassword ? true : false}
                    style={{ opacity: !validEmail || !validPassword ? 0.5 : 1 }}
                >Create Account
                </button>
                <div aria-live="polite" aria-atomic="true">
                    {state.errors?.email ? (<p className="mt-2 text-sm text-red-500">{state.errors.email}</p>) : null}
                </div>
                <Link className='text-sky-700 text-xs' href={'/createaccount'}>Create new account</Link>
            </form>
    )
};
