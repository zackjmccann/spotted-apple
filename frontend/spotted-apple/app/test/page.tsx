'use client';

import { useActionState } from 'react'
import { Banner } from '@/features/banner-feature'
import { TestProps } from '@/features/test/types'
import { testAction } from '@/features/test/actions'
import TestForm from '@/features/test/form'


export default function Page() {
  const testProps: TestProps = {action: testAction}

  return (
    <main className="flex min-h-screen flex-row items-center justify-around p-12">
        <Banner />
        <TestForm {...testProps}/>
    </main>
  );
};
