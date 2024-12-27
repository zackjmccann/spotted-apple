import { CreateAccountFormSchema } from '@/features/create-account-form-feature/schemas'
import { SignUpState } from '@/features/sign-up-feature/types'
import { checkIfEmailExists } from '@/data-access/auth/auth'

function validateFields(formData: FormData) {
    return CreateAccountFormSchema.safeParse({
        email: formData.get('email'),
        firstName: formData.get('firstName'),
        lastName: formData.get('lastName'),
    })
}

export async function createAccount(prevState: SignUpState, formData: FormData,) {
    const validatedFields = validateFields(formData);
    const enterValues: { [key: string]: string } = {};
    formData.forEach((value, key) => { enterValues[key] = value.toString(); });

    if (!validatedFields.success) {
        const formErrors = validatedFields.error.flatten().fieldErrors;
        return {
            created: false,
            passwordSet: false,
            errors: formErrors,
            formData: enterValues};
    };
        
    // Check user email
    const emailExists: boolean | null = await checkIfEmailExists(enterValues.email);

    if(emailExists == null) {
        return {
            created: false,
            passwordSet: false,
            errors: {email: ['An error occurred during email registration check.']},
            formData: enterValues};
    }

    if(emailExists) {
        return {
            created: false,
            passwordSet: false,
            errors: {email: ['Email already exists. Please login.']},
            formData: enterValues};
    }

    return { created: true, passwordSet: false, formData: enterValues, } as SignUpState;
};