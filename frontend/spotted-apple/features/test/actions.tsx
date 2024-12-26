import { TestFormState } from '@/features/test/types';
import { RequestParameters } from "@/data-access/types";
import { authService } from '@/data-access/auth/service';


export async function testFormAction(prevState: TestFormState, formData: FormData,) {
    const email = formData.get('email')
    console.log(`Entered Email: ${email}`)

    const checkIfEmailIsRegisteredRequest: RequestParameters = {
        method: 'POST',
        endpoint: '/register/introspect',
        body: {email: email?.toString() ?? 'none'}
    }

    const emailIsRegistered = await authService(checkIfEmailIsRegisteredRequest);
    console.log(`Email is regesistered: ${emailIsRegistered['registered']}`)
    return prevState
}


type Slug = { slug: string }
type SlugType = { params: Promise<Slug> }

export default async function Page( { params }: SlugType ) {
    const slug = (await params).slug
    return <div>My Post: {slug}</div>
  }