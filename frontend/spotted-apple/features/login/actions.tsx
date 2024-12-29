import { LoginFormSchema } from '@/features/login/schemas'
import { LoginState } from '@/features/login/types'

function validateFields(formData: FormData) {
    return LoginFormSchema.safeParse({
        email: formData.get('email'),
        password: formData.get('password'),
    })
}

export async function login(prevState: LoginState, formData: FormData,) {
    const validatedFields = validateFields(formData);
    const enterValues: { [key: string]: string } = {};
    formData.forEach((value, key) => { enterValues[key] = value.toString(); });

    if (!validatedFields.success) {
        const formErrors = validatedFields.error.flatten().fieldErrors;
        return { errors: formErrors, formData: enterValues};
    };
    
    // Login logic
    // 
    
    return prevState;
};