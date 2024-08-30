import { cn } from '@/lib/utils';
import { useState } from 'react';

type SearchCardProps = {
  advancedSearchWidth: string;
  maxCardHeight: string;
};

type SearchSwicthProps = {
  advancedToggled: boolean;
  setAdvancedToggled: (advancedToggled: boolean) => void;
};

export function SearchSwitch({
  advancedToggled,
  setAdvancedToggled,
}: SearchSwicthProps) {
  return (
    <div>
      <button
        className={cn(
          'py-2 px-5 rounded-tl-lg transition duration-300',
          !advancedToggled
            ? 'bg-highlight-blue text-white'
            : 'bg-white text-slate-400',
          advancedToggled ? 'hover:bg-highlight-blue/[0.1]' : '',
        )}
        onClick={() => setAdvancedToggled(false)}
      >
        Search
      </button>
      <button
        className={cn(
          'py-2 px-5 transiiton duration-300 rounded-br-lg',
          advancedToggled
            ? 'bg-highlight-blue text-white'
            : 'bg-white text-slate-400',
          !advancedToggled ? 'hover:bg-highlight-blue/[0.1]' : '',
        )}
        onClick={() => setAdvancedToggled(true)}
      >
        Advanced Search
      </button>
    </div>
  );
}

export function SearchCard(props: SearchCardProps) {
  const [advancedToggled, setAdvancedToggled] = useState(false);

  return (
    <>
      <SearchSwitch
        advancedToggled={advancedToggled}
        setAdvancedToggled={setAdvancedToggled}
      />
      <div
        className="overflow-y-auto"
        style={{ maxHeight: props.maxCardHeight }}
      ></div>
    </>
  );
}
