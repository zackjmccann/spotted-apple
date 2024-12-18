'use client';

import { SignUpState} from '@/features/sign-up-feature/types';
import { SignUpProps } from '@/features/sign-up-feature/types';
import signUp from '@/features/sign-up-feature/actions';

import CreateAccountForm from '@/features/create-account-form-feature/form';
import SetPasswordForm from '@/features/create-set-password-form-feature/form'

const Banner = () => {
  return (
    <div className="relative z-[-1] flex place-items-center before:absolute before:h-[300px] before:w-full before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-full after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 sm:before:w-[480px] sm:after:w-[240px] before:lg:h-[360px]">
      <div className="flex flex-col items-center">
        <h1 className="mb-3 text-6xl font-semibold">
          Spotted Apple
        </h1>
        <p>Free your music today</p>
      </div>
    </div>
  )
};

export default function Page() {
  const initialSignUpState: SignUpState = {created: false, passwordSet: false};
  const signUpProps: SignUpProps = signUp(initialSignUpState)

  return (
    <main className="flex min-h-screen flex-row items-center justify-around p-12">
        <Banner />
        {!signUpProps.state.created ? <CreateAccountForm {...signUpProps}/> : <SetPasswordForm {...signUpProps}/>}
    </main>
  );
};
