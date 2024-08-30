import { FilterContext } from '@/lib/context/FilterContext';
import { useFulltextSearchQuery } from '@/lib/hooks/parser';
import { Search } from 'lucide-react';
import { useRouter } from 'next/router';
import { useContext, useEffect, useState } from 'react';
import { Button } from '../ui/button';
import { SearchFilter } from './filter';
import { fetchAutocompleteData } from './autocomplete';

export function FulltextSearch({
  input = '',
  onChangeInput,
}: {
  input: string;
  onChangeInput: (input: string) => void;
}) {
  const filterContext = useContext(FilterContext);
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    onChangeInput(e.target.value);
  };

  const [autocompleteSuggestions, setAutocompleteSuggestions] = useState<
    string[]
  >([]);

  useEffect(() => {
    const fetchCompletions = async () => {
      try {
        setAutocompleteSuggestions(await fetchAutocompleteData(input, ''));
        console.log(autocompleteSuggestions);
      } catch (e) {
        console.error(e);
      }
    };
    if (input.length > 0) fetchCompletions();
    else setAutocompleteSuggestions([]);
  }, [input]);

  return (
    <form
      className="p-[2rem] grid grid-rows-2 gap-y-3"
      onSubmit={(e) => {
        e.preventDefault();
        router.push(useFulltextSearchQuery(input, filterContext.filter));
      }}
    >
      <div className="flex">
        <input
          list={'autocomplete-suggestions'}
          className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
          placeholder="Please enter the keyword you would like to look for..."
          onChange={handleChange}
          value={input}
        />
        <datalist id={'autocomplete-suggestions'}>
          {autocompleteSuggestions.map((suggestion, index) => (
            <option key={index} value={suggestion} />
          ))}
        </datalist>
        <Button className="bg-highlight-blue ml-4">
          <Search color="white" />
        </Button>
      </div>
      <SearchFilter />
    </form>
  );
}
