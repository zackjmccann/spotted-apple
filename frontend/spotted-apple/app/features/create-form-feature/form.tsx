'use client';

import { ChangeEvent, useActionState, useState, } from 'react'
import { FormField, FormFieldError, SubmitButton } from '@/app/features/create-form-feature/components'
import { InputFields, ButtonDisplay } from '@/app/features/create-form-feature/types'
import { CreateAccountState, InputFieldErrorState } from '@/app/features/create-form-feature/types';
import { createAccount } from '@/app/features/create-form-feature/actions';

export default function CreateAccountForm() {
    const initialState: CreateAccountState = {created: false};
    const initialErrorState: InputFieldErrorState = {email: true, firstName: true, lastName: true};
    const [state, formAction] = useActionState(createAccount, initialState);
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
        console.log(`errorState 2: ${JSON.stringify(errorState)}`)
    };

    const fields: InputFields = [
        {
            id: 'email',
            placeHolder: 'example@email.com',
            initialValue: intputState ? intputState.email.toString() : "",
            onChange: onChange,
        },
        {
            id: 'firstName',
            placeHolder: 'First Name',
            initialValue: intputState ? intputState.firstName.toString() : "",
            onChange: onChange
        },
        {
            id: 'lastName',
            placeHolder: 'Last Name',
            initialValue: intputState ? intputState.lastName.toString() : "",
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
            <SubmitButton key='createAccountSubmittButton' {...buttonValues}/>
        </form>
    )
};
