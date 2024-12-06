"use client";

import { useRef, useEffect, useState } from 'react';

type CustomFunctionalComponentProps = {
    id: string;
    name: string | undefined;

}

function CustomFunctionalComponent(props: CustomFunctionalComponentProps) {
    const [state, setState] = useState(0)
    const id: string = props.id
    const name: string | undefined = props.name

    const formattedName = name + '!'

    const clickButton = useRef<HTMLButtonElement>(null)
    const clickIt = () => (clickButton.current ? console.log('clicked!') : null)

    useEffect(
        () => {
            console.log(state)
            return () => {
                if(state > 10) {
                    console.log('Goodbye!')
                }
            }
        },
        [state]
    )

    if (state < 5) {
        console.log('here!')
        clickIt()
        console.log(`state: ${state}`)

    }

    return (
        <div>
            <h2>Here's a Functional Component</h2>
            <p id={id}>My name is {formattedName} and my state is {state} </p>
            <button ref={clickButton} onClick={() => setState(state + 1)}>Click</button>
        </div>
    )
};

export default function Page() {
    const customProps: CustomFunctionalComponentProps = {id: 'customId', name: 'Custom Component'}
    return (
        <main className="flex min-h-screen flex-col items-center p-12">
            <div className="flex flex-col items-center">
                <h1 className="mb-3 text-6xl font-semibold"> Spotted Apple Test Page </h1>
            </div>
            <CustomFunctionalComponent
                id={customProps.id}
                name={customProps.name}
            />
    </main>
  );
};