'use client';

import { ChangeEvent, useState, } from 'react'
import { FormField, SubmitButton } from '@/lib/forms/components'
import { ButtonDisplay, InputFields, InputFieldErrorState} from '@/lib/forms/types'
import { LoginProps } from '@/features/login/types';
import { FaEye, FaEyeSlash } from "react-icons/fa";


export default function LoginForm({state, action}: LoginProps) {
    const initialErrorState: InputFieldErrorState = {email: true, password: true};
    const [intputState, setInput] = useState(state.formData);
    const [errorState, displayError] = useState(initialErrorState) 
    const [showPassword, setShowPassword] = useState('password');

    const onSubmit = () => { displayError(initialErrorState) }

    const handleToggle = () => {
        if (showPassword === 'password') {
            setShowPassword('text');
        } else {
           setShowPassword('password');
        }
     };
    const onChange = (e: ChangeEvent<HTMLInputElement>) => {
        const currentlySelectedInputField = e.target.name;
        const currentlySelectedValue = e.target.value;
        let enteredValueIsBlank: boolean = true;

        setInput(currentInput => ({ ...currentInput, [currentlySelectedInputField]: currentlySelectedValue }))
        
        if (currentlySelectedValue.trim() != "" ||
            currentlySelectedValue != "" ||
            currentlySelectedValue != undefined ||
            currentlySelectedValue != null
        ) { 
            enteredValueIsBlank = false;
        }

        if (state.errors && state.errors[currentlySelectedInputField]) {
            displayError(currentDisplay => ({ ...currentDisplay, [currentlySelectedInputField]: enteredValueIsBlank }))
        }
    };

    const fields: InputFields = [
        {
            id: 'email',
            initialValue: intputState && intputState.email ? intputState.email : "",
            placeHolder: 'Email',
            onChange: onChange,
        },
        {
            id: 'password',
            fieldType: showPassword,
            placeHolder: 'Password',
            onChange: onChange
        },
    ]

    const formId = 'login';
    const formHeader = 'Log into your account';
    const buttonValues: ButtonDisplay = {staticDisplay: 'Login', pendingDisplay: 'logging in...'}
    const errorMessage: string = 'Email and/or Password Invlaid.'

    return (
        <form id={formId} className={formId} action={action} onSubmit={onSubmit}>
            <p>{formHeader}</p>
            <ul>{fields.map((field) => (
                <div key={`${field.id}Container`} id={`${field.id}Container`} className="flex">
                    <FormField key={field.id} {...field}/>
                    {field.id != 'password' ? null :
                    <span id='showPassWordToggle' onClick={handleToggle}>
                    {showPassword != 'password' ? <FaEyeSlash id='passWordToggleIcon'/> : <FaEye id='passWordToggleIcon'/>}
                    </span>
                    }
                </div>
                ))}
            </ul>
            {state.errors ? <p key='LoginError' className='errorField'>{errorMessage}</p> : null }
            <SubmitButton key='loginSubmitButton' {...buttonValues}/>
        </form>
    )
};
