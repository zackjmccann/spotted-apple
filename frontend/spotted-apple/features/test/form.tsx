'use client';

import { FormField, SubmitButton } from '@/lib/forms/components'
import { ButtonDisplay, InputFields } from '@/lib/forms/types'
import { TestProps } from '@/features/test/types';


export default function TestForm({action}: TestProps) {
    const fields: InputFields = [
        {
            id: 'testField',
            placeHolder: 'Test Field',
        }
    ]

    const formId = 'test';
    const formHeader = 'Test Form';
    const buttonValues: ButtonDisplay = {staticDisplay: 'Test', pendingDisplay: 'testing...'}

    return (
        <form id={formId} className={formId} action={action}>
            <p>{formHeader}</p>
            <ul>{fields.map((field) => (
                <div key={`${field.id}Container`} id={`${field.id}Container`} className="flex">
                    <FormField key={field.id} {...field}/>
                </div>
                ))}
            </ul>
            <SubmitButton key='loginSubmitButton' {...buttonValues}/>
        </form>
    )
};
