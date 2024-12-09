"use client";

import { CustomFunctionalComponent, CustomFunctionalComponentProps } from '@/features/test'

export default function Page() {
    const customProps: CustomFunctionalComponentProps = {id: 'customId', name: 'Custom Component'}
    return (
        <div className="flex min-h-screen flex-col items-center p-12">
            <div className="flex flex-col items-center">
                <h1 className="mb-3 text-6xl font-semibold"> Spotted Apple Test Page </h1>
            </div>
            <CustomFunctionalComponent
                id={customProps.id}
                name={customProps.name}
            />
        </div>
  );
};