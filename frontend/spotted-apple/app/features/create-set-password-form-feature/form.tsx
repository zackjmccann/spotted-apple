'use client';

import { ChangeEvent, useActionState, useState, } from 'react'
import { SetPasswordState } from '@/app/features/create-set-password-form-feature/types';
import { FormField, FormFieldError, SubmitButton } from '@/app/lib/forms/components'
import { ButtonDisplay, InputFields, InputFieldErrorState} from '@/app/lib/forms/types'
import { setPassword } from '@/app/features/create-set-password-form-feature/actions';

export default function SetPasswordForm() {
    // TODO: Display one error message at the bottom, not per field
    const initialState: SetPasswordState = {passwordSet: false};
    const initialErrorState: InputFieldErrorState = {email: true, passWord: true, confirmPassword: true};
    const [state, formAction] = useActionState(setPassword, initialState);    
    const [intputState, setInput] = useState(state.formData);
    const [errorState, displayError] = useState(initialErrorState) 

    const onSubmit = () => { displayError(initialErrorState) }

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
            initialValue: intputState ? intputState.email.toString() : "",
            onChange: onChange,
        },
        {
            id: 'password',
            initialValue: intputState ? intputState.password.toString() : "",
            onChange: onChange
        },
        {
            id: 'confirmPassword',
            initialValue: intputState ? intputState.confirmPassword.toString() : "",
            onChange: onChange
        },
    ]

    const formId = 'setPassword';
    const formHeader = 'Set a password for your account';
    const buttonValues: ButtonDisplay = {staticDisplay: 'Set Password', pendingDisplay: 'setting password...'}

    return (
        <form id={formId} className={formId} action={formAction} onSubmit={onSubmit}>
            <p>{formHeader}</p>
            <ul>{fields.map((field) => (
                <div key={`${field.id}Container`}>
                    <FormField key={field.id} {...field}/>
                    {state.errors && errorState[field.id] ?
                     <FormFieldError key={`${field.id}Error`} errors={state.errors[field.id]} />
                     :
                     null
                    }
                </div>
                ))}
            </ul>
            <SubmitButton key='setPasswordSubmitButton' {...buttonValues}/>
        </form>
    )
};
