'use client';

import { useRef, useState, useEffect } from "react";
import {Icon} from 'react-icons-kit';
import {eye} from 'react-icons-kit/feather/eye';
import {eyeOff} from 'react-icons-kit/feather/eyeOff';
import { useFormState } from 'react-dom'
import { createAccount, CreateAccountState } from '@/app/lib/create-account-actions';
import styles from '@/app/ui/styles.module.css'

export default function CreateForm() {
    const PASSWORD_REGEX = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!~@#$%]).{8,24}$/;;
    const initialState: CreateAccountState = { message: null, errors: {} };
    
    const userRef = useRef<HTMLInputElement>(null);

    const [firstName, setFirstName] = useState('')
    const [validFirstName, setValidFirstName] = useState(false)
    
    const [lastName, setLastName] = useState('')
    const [validLastName, setValidLastName] = useState(false)
    
    const [email, setEmail] = useState('')
    const [validEmail, setValidLEmail] = useState(false)

    const [password, setPassword] = useState('');
    const [validPassword, setValidPassword] = useState(false);

    const [showPassword, setShowPassword] = useState('password');
    const [icon, setIcon] = useState(eyeOff);
    
    const [passwordConfirmation, setPasswordConfirmation] = useState('');
    const [validPasswordConfirmation, setValidPasswordConfirmation] = useState(false);
    const [passwordConfirmationFocus, setPasswordConfirmationFocus] = useState(false);

    const [state, formAction] = useFormState(createAccount, initialState);

    useEffect(() => {
        if(userRef.current) {
            userRef.current.focus()
        }
    }, [])

    useEffect(() => {
       const firstNameEntry = firstName.length != 0
        setValidFirstName(firstNameEntry);
    }, [firstName])

    useEffect(() => {
       const lastNameEntry = lastName.length != 0
        setValidLastName(lastNameEntry);
    }, [lastName])

    useEffect(() => {
       const emailEntry = email.length != 0 // TODO: This isn't a good check
        setValidLEmail(emailEntry);
    }, [email])

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

    useEffect(() => {
        setValidPassword(PASSWORD_REGEX.test(password));
        setValidPasswordConfirmation(password === passwordConfirmation);
    }, [password, passwordConfirmation])

    return (
            <form className={styles.form} action={formAction}>
                <label htmlFor='firstName' hidden>First Name</label>
                <input
                    name='firstName'
                    id='firstName'
                    type='string'
                    placeholder='First Name'
                    onChange={(e) => setFirstName(e.target.value)}
                    value={firstName}
                    required
                    aria-invalid={validFirstName ? 'false' : 'true'}
                    aria-describedby='firstNameNote'
                />
                <label htmlFor='lastName' hidden>Last Name</label>
                <input
                    name='lastName'
                    id='lastName'
                    type='string'
                    placeholder='Last Name'
                    onChange={(e) => setLastName(e.target.value)}
                    value={lastName}
                    required
                    aria-invalid={validLastName ? 'false' : 'true'}
                    aria-describedby='lastNameNote'
                />
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
                <label htmlFor='passwordConfirmation' hidden>Password Confirmation</label>
                <input
                    name='passwordConfirmation'
                    id='passwordConfirmation'
                    type={showPassword}
                    placeholder='Password Confirmation'
                    onChange={(e) => setPasswordConfirmation(e.target.value)}
                    value={passwordConfirmation}
                    required
                    aria-invalid={validPasswordConfirmation ? 'false' : 'true'}
                    aria-describedby='passwordConfirmationNote'
                    onFocus={() => setPasswordConfirmationFocus(true)}
                /> 
                <p 
                    id='passwordConfirmationNote'
                    className={styles.passwordConfirmationNote}
                >{passwordConfirmationFocus && !validPasswordConfirmation ? 'Passwords do not match' : null}
                </p>
                <button
                    className='w-full h-10 font-semibold rounded-lg bg-[#0141ff]'
                    type="submit"
                    disabled={!validFirstName || !validLastName || !validPassword || !validPasswordConfirmation ? true : false}
                    style={{ opacity: !validFirstName || !validLastName || !validPassword || !validPasswordConfirmation ? 0.5 : 1 }}
                >Create Account
                </button>
                <div aria-live="polite" aria-atomic="true">
                    {state.errors?.email ? (<p className="mt-2 text-sm text-red-500">{state.errors.email}</p>) : null}
                </div>
                <p className='text-sky-700 text-xs'>Already have an account? Sign in</p>
            </form>
    )
};
