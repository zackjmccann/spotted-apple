"use client";

import { useFormStatus } from 'react-dom'
import { InputField, ButtonDisplay, InputFieldsErrors} from '@/lib/forms/types'

export function FormField({id, placeHolder, initialValue, fieldType, onChange}: InputField) {
    return (<input
                id={`${id}Input`}
                name={id}
                placeholder={placeHolder}
                value={initialValue}
                type={fieldType}
                onChange={onChange ? (ev: any) => onChange(ev) : undefined}
            />
    )
}

export function FormFieldError({ errors }: InputFieldsErrors) {
    if(errors) {
        const errorMessage = errors.join(',');
        return(<p className='errorField'>{errorMessage}</p>)
    }
}

export function SubmitButton({staticDisplay, pendingDisplay}: ButtonDisplay) {
    const { pending } = useFormStatus()
    return (
      <button type="submit" disabled={pending}>
        {pending ? pendingDisplay : staticDisplay}
      </button>
    )
};