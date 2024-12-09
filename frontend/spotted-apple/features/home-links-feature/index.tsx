import Link from 'next/link';
import { CustomLink } from '@/features/home-links-feature/schema'

const createAccount: CustomLink = {
    name: 'Create Account',
    key: 'create-account',
    href: `/create-account`,
    description: 'Get started with Spotted Apple and share music faster.',
};

const logIn: CustomLink = {
    name: 'Login',
    key: 'login',
    href: '/login',
    description: 'Already a user? Log in to access your account.',
};

const howItWorks: CustomLink = {
    name: 'How it Works',
    key: 'how-it-works',
    href: '/',
    description: 'Learn about Spotted Apple and our music sharing approach.',
};

const about: CustomLink = {
    name: 'About',
    key: 'about',
    href: '/',
    description: 'Explore Spotted Apple and our mission.',
}

const links: CustomLink[] = [
    createAccount,
    logIn,
    howItWorks,
    about,
];

export default function HomeLinks() { 
    return (
        <>
        {links.map((link) => {
          return (
            <h2 className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
                key={link.key}
            >
                <Link href={link.href}>
                <p className="mb-3 text-2xl font-semibold">
                    {link.name}
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
};
