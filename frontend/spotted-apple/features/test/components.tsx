import { FormField, SubmitButton } from '@/lib/forms/components'
import { ButtonDisplay, InputFields} from '@/lib/forms/types'
import { TestFormProps } from '@/features/test/types';

export function TestForm({state, formAction}: TestFormProps) {
    const fields: InputFields = [ {id: 'email', placeHolder: 'example@email.com',}, ]
    const formId = 'testForm';
    const formHeader = 'Testing a Backend Server Request';
    const buttonValues: ButtonDisplay = {staticDisplay: 'Check Email', pendingDisplay: 'checking email...'}

    return (
        <form id={formId} className={formId} action={formAction}>
            <p>{formHeader}</p>
            <ul>{fields.map((field) => (
                <div key={`${field.id}Container`}>
                    <FormField key={field.id} {...field}/>
                </div>
                ))}
            </ul>
            <SubmitButton key='testFormSubmitButton' {...buttonValues}/>
        </form>
    )
};