export function PassowrdFormFieldError(errors: Record<string, string[]>) {
    let errorMessage: string;

    // Only display the first error message.
    // If the subsequent entries continue to fail, the
    // validation will continue to flag the errors, which 
    // can be correct one at a time.

    // Only display the confirmPassword error (non matching passwords)
    // if the initial password input is valid.
    if(errors['password']) {
        errorMessage = errors['password'][0]
    } else {
        errorMessage = errors['confirmPassword'][0]
    }
    return(<p key='PasswordEntryError' className='errorField'>{errorMessage}</p>)
}