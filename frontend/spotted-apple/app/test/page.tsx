"use client";

import { useActionState } from 'react'
import { TestForm } from '@/features/test/components'
import { testFormAction } from '@/features/test/actions'

export default function Page() {
    const initialState = {}
    const [state, formAction] = useActionState(testFormAction, initialState)

    return (
        <div className="flex min-h-screen flex-col items-center justify-around p-12">
            <div className="flex flex-col items-center">
                <h1 className="mb-3 text-6xl font-semibold"> Spotted Apple Test Page </h1>
            </div>
            <TestForm state={state} formAction={formAction}/>
        </div>
  );
};