'use client';

import Link from 'next/link';

const links = [
    { 
        key: 'create-account',
        name: 'Create Account',
        href: '/create-account',
        description: 'Get started with Spotted Apple and share music faster.'
      },
      {
        key: 'login',
        name: 'Login',
        href: '/login',
        description: 'Already a user? Log in to access your account.'
      },
      { 
        key: 'how-it-works',
        name: 'How it Works',
        href: '/',
        description: 'Learn about Spotted Apple and our music sharing approach.'
      },
      { 
        key: 'about',
        name: 'About',
        href: '/',
        description: 'Explore Spotted Apple and our mission.'
    },
  ];

  export default function HomeLinks() {  
    return (
      <>
        {links.map((link) => {
          return (
            <h2 className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                key={link.key}
            >
                <Link
                href={link.href}
                >
                <p className="mb-3 text-2xl font-semibold">{link.name}
                    <span className="inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none">
                        -&gt;
                    </span>
                </p>
                <p className="m-0 max-w-[30ch] text-sm opacity-50">
                    {link.description}
                </p>
                </Link>
            </h2>
          );
        })}
      </>
    );
  }
