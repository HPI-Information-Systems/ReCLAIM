import Image from 'next/image';
import Link from 'next/link';
import { useState } from 'react';

type DropdownProps = {
  search: { visable: boolean; name: string; link: string };
  aboutDatabase: { visable: boolean; name: string; link: string };
  aboutJDCRP: { visable: boolean; name: string; link: string };
  help: { visable: boolean; name: string; link: string };
};

export default function Dropdown({
  search,
  aboutDatabase,
  aboutJDCRP,
  help,
}: DropdownProps) {
  const items = [search, aboutDatabase, aboutJDCRP, help];

  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const toggleDropdown = () => {
    setIsDropdownOpen((prev) => !prev);
  };

  return (
    <div className="inline-flex bg-white border rounded-md mr-2 mt-2">
      <div className="relative">
        <button
          type="button"
          onClick={toggleDropdown}
          className="inline-flex items-center justify-center h-full px-2 text-highlight-blue rounded-r-md hover:bg-zinc-200"
        >
          <Link
            href="#"
            className="px-4 py-2 text-sm text-highlight-blue hover:text-gray-700 hover:bg-zinc-200 rounded-l-md"
          >
            Menu
          </Link>
          <Image src="/list.svg" alt="list icon" width={20} height={20} />
        </button>

        {isDropdownOpen && (
          <div className="absolute right-0 z-10 w-56 mt-4 origin-top-right bg-white border border-gray-100 rounded-md shadow-lg">
            <div className="p-2">
              {items.map(
                (item, index) =>
                  item.visable && (
                    <Link
                      className="block px-4 py-2 text-md text-highlight-blue rounded-lg hover:bg-zinc-200 hover:text-gray-700"
                      key={index}
                      href={item.link}
                    >
                      {item.name}
                    </Link>
                  ),
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
