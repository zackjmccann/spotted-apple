'use client' // Error boundaries must be Client Components

import logger from '@/lib/logging'
import { useEffect } from 'react'
 
export default function GlobalError({ error, reset, }: { error: Error & { digest?: string }; reset: () => void }) {
  useEffect(() => { logger.error(error) }, [error])

  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={ () => reset() }> Try again </button>
    </div>
  )
}
