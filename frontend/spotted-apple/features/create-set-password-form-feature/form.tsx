'use client';

import { ChangeEvent, useState, } from 'react'
import { FormField, FormFieldError, SubmitButton } from '@/lib/forms/components'
import { ButtonDisplay, InputFields, InputFieldErrorState} from '@/lib/forms/types'
import { SetPasswordFormProps } from '@/features/create-set-password-form-feature/types';


export default function SetPasswordForm({state, formAction}: SetPasswordFormProps) {
    // TODO: Display one error message at the bottom, not per field
    const initialErrorState: InputFieldErrorState = {email: true, password: true, confirmPassword: true};
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
            initialValue: intputState && intputState.email ? intputState.email : "",
            onChange: onChange,
        },
        {
            id: 'password',
            onChange: onChange
        },
        {
            id: 'confirmPassword',
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
