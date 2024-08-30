import { cn } from '@/lib/utils';
import Link from 'next/link';
import Dropdown from '@/components/general/headerDropdown';

type HeaderProps = {
  logoOverflowHidden: boolean;
};

export function Header({ logoOverflowHidden }: HeaderProps) {
  return (
    <header
      className={cn(
        'bg-white w-full h-16',
        logoOverflowHidden ? 'shadow-md' : '',
      )}
    >
      <div className="container p-0 mx-auto flex items-center relative h-full w-full ">
        <Link href="/">
          <div
            className={cn(
              'p-2 rounded-b-md bg-white',
              logoOverflowHidden
                ? 'w-[160px] h-12'
                : 'z-10 w-[170px] h-40 top-0 absolute',
            )}
          >
            <div
              className={cn(
                'bg-cover w-full h-full',
                logoOverflowHidden ? 'bg-jdcrp-logo-cut' : 'bg-jdcrp-logo',
              )}
            ></div>
          </div>
        </Link>
        <div className="grow"></div>
        <div className="max-lg:hidden">
          <Link className={`m-5 text-lg text-highlight-blue`} href="/search">
            Search
          </Link>
          <Link className={`m-5 text-lg text-highlight-blue`} href="/about">
            About the Database
          </Link>
          <Link
            className={`m-5 text-lg text-highlight-blue`}
            href="https://jdcrp.org/"
          >
            About JDCRP
          </Link>
          <Link className={`m-5 text-lg text-highlight-blue`} href="/help">
            Help
          </Link>
        </div>
        <div className="lg:hidden">
          <Dropdown
            search={{ visable: true, name: 'Search', link: '/search' }}
            aboutDatabase={{
              visable: true,
              name: 'About the Database',
              link: '/',
            }}
            aboutJDCRP={{
              visable: true,
              name: 'About JDCRP',
              link: 'https://jdcrp.org/',
            }}
            help={{ visable: true, name: 'Help', link: '/help' }}
          />
        </div>
      </div>
    </header>
  );
}
