import bcrypt from 'bcrypt';

export async function hashPassword(password: string): Promise<Array<String>> {
    const salt = bcrypt.genSaltSync(10);
    const hash = bcrypt.hashSync(password, salt);
    return [hash, salt]
}

export async function validPasswordEntry(enteredPassword: string, userPassword: string): Promise<Boolean> {
    return bcrypt.compareSync(enteredPassword, userPassword);
}