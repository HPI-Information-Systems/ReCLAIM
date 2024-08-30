import { createContext } from 'react';
import { Filter } from '../types/filter';

type FilterContext = {
  filter?: Filter;
  setFilteredSources: (sources: string[]) => void;
  addFilteredSource: (source: string) => void;
  removeFilteredSource: (source: string) => void;
  setOnlyImages: (onlyImages: boolean) => void;
  toggleOnlyImages: () => void;
};

export const FilterContext = createContext<FilterContext>({
  filter: undefined,
  setFilteredSources: () => {},
  addFilteredSource: () => {},
  removeFilteredSource: () => {},
  setOnlyImages: () => {},
  toggleOnlyImages: () => {},
});
