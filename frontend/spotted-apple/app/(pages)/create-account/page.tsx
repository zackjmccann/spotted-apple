import CreateAccountForm from '@/app/features/create-form-feature/form';

import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Create Account',
};

export default async function Page() {
  const isAccountCreated = false;
  return (
    <main className="flex min-h-screen flex-row items-center justify-around p-12">
        <div className="relative z-[-1] flex place-items-center before:absolute before:h-[300px] before:w-full before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-full after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 sm:before:w-[480px] sm:after:w-[240px] before:lg:h-[360px]">
          {/* TODO: Abstract the div element below and render via component */}
          <div className="flex flex-col items-center">
            <h1 className="mb-3 text-6xl font-semibold">
              Spotted Apple
            </h1>
            <p>Free your music today</p>
          </div>
        </div>
        <CreateAccountForm />
    </main>
  );
};