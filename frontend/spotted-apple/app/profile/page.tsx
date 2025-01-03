'use client';

import { Banner } from '@/features/banner-feature'
export default function Page() {
  return (
    <main className="flex min-h-screen flex-row items-center justify-around p-12">
        <Banner />
        <h1>Profile</h1>
    </main>
  );
};
