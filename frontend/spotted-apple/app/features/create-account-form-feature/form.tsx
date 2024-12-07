'use client';

import { ChangeEvent, useState, } from 'react'
import { FormField, FormFieldError, SubmitButton } from '@/app/lib/forms/components'
import { ButtonDisplay, InputFields, InputFieldErrorState} from '@/app/lib/forms/types'
import { CreateAccountFormProps } from '@/app/features/create-account-form-feature/types';

export default function CreateAccountForm({state, formAction}: CreateAccountFormProps) {
    const initialErrorState: InputFieldErrorState = {email: true, firstName: true, lastName: true};
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
            placeHolder: 'example@email.com',
            initialValue: intputState && intputState.email ? intputState.email : "",
            onChange: onChange,
        },
        {
            id: 'firstName',
            placeHolder: 'First Name',
            initialValue: intputState && intputState.firstName ? intputState.firstName : "",
            onChange: onChange
        },
        {
            id: 'lastName',
            placeHolder: 'Last Name',
            initialValue: intputState && intputState.lastName ? intputState.lastName : "",
            onChange: onChange
        },
    ]

    const formId = 'createAccount';
    const formHeader = 'Create an account with Spotted Apple';
    const buttonValues: ButtonDisplay = {staticDisplay: 'Create Account', pendingDisplay: 'creating account...'}

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
            <SubmitButton key='createAccountSubmitButton' {...buttonValues}/>
        </form>
    )
};
