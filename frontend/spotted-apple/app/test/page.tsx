"use client";

import { useState } from 'react'
import { authenticateWithBackend, setAuthenticationCookies } from '@/features/auth/auth'


export default function Page() {
    type authResponse = { access_token?: string, refresh_token?: string }
    const initalState: authResponse = {access_token: '', refresh_token: ''}
    const [state, setState] = useState(initalState)
    
    const click = async () => {
        setState(await authenticateWithBackend())
        setAuthenticationCookies(state)
    }
    return (
        <div className="flex min-h-screen flex-col items-center p-12">
            <div className="flex flex-col items-center justify-between p-6">
                <h1 className="mb-3 text-6xl font-semibold"> Spotted Apple Test Page </h1>
                <p>Access Token: {state.access_token!.slice(-10)}</p>
                <p>Refresh Token: {state.refresh_token!.slice(-10)}</p>
                <button onClick={click}>Get Token</button>
            </div>
        </div>
  );
};
