'use client';

import { createAccount, CreateAccountState } from '@/app/modules/create-account/create-account-actions';
import { useFormStatus, useFormState } from 'react-dom'

function SubmitButton() {
    const { pending } = useFormStatus()
  
    return (
      <button type="submit" disabled={pending}>
        {pending ? 'creating account...' : 'Create Account'}
      </button>
    )
};

interface Field {
    name: string,
    placeHolder: string,
}

function FormField(field: Field, error: string[] | undefined) {
    return (
        <div>
            <input key={field.name} name={field.name} placeholder={field.placeHolder}/>
            {field.name in error! ? (<p className='errorField'>{error}</p>) : <></>}
        </div>
    )
}

export default function CreateAccountForm() {
    const initialState: CreateAccountState = {created: false};
    const [state, formAction] = useFormState(createAccount, initialState); 
    
    const errors = state.errors;

    const fields = [
        {name: 'email', placeHolder: 'example@email.com'} as Field,
        {name: 'firstName', placeHolder: 'First Name'} as Field,
        {name: 'lastName', placeHolder: 'Last Name'} as Field,
    ]

    // const formFields = fields.map(field => 
    //     <div>
    //         <input name={field.name} placeholder={field.placeHolder}/>
    //         {field.name in errors! ? (<p className='errorField'>{errors[field.name]}</p>) : <></>}
    //     </div>
    // );

    return (
        <form className='createAccount' action={formAction}>
            <p>Create an account with Spotted Apple</p>
            <ul>{[fields, errors].map((field, error) => <FormField name={field.name} placeHolder={field.placeHolder} error={error}/>)}</ul>
            <SubmitButton />
        </form>
    )
};
