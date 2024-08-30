import { AVAILABLE_SOURCES } from '@/lib/config/sources';
import { FilterContext } from '@/lib/context/FilterContext';
import { Filter } from '@/lib/types/filter';
import { urlSearchFieldDelimiter } from '@/pages/search';
import { useContext, useState } from 'react';
import { AdvancedSearch } from './advancedSearch';
import { FulltextSearch } from './fulltextSearch';
import { SearchSwitch } from './searchSwitch';

export type FormDataEntry = {
  topicName: string | null;
  value: string;
  mode: 'contains' | 'does not contain';
};

/**
 * Parses a query parameter string from a URL into a FormDataEntry object.
 * @param queryParams The query parameter string to parse
 * @returns The query parameter as a parsed FormDataEntry for the frontend input fields
 */
function parseQueryTopicParams(queryParams: string): FormDataEntry {
  // Each query parameter has the format: [!][topic]:<value>,
  // where the colon is the delimiter specified in urlSearchFieldDelimiter.
  // The '!' is optional and stands for 'does not contain'.
  const queryParamsSplit = queryParams.split(urlSearchFieldDelimiter);

  // Extract all the query parameters as mentioned above
  const isModusContains = queryParamsSplit[0][0] !== '!';
  const topicName = isModusContains
    ? queryParamsSplit[0]
    : queryParamsSplit[0].substring(1);

  const value = queryParamsSplit[1];

  const entry = {
    topicName: topicName,
    value: value,
    mode: (isModusContains ? 'contains' : 'does not contain') as
      | 'contains'
      | 'does not contain',
  };
  return entry;
}

/**
 * Extract the values for the search box from the URL query parameters
 * @param searchQuery URL query parameters
 * @returns State variables to use for the search box
 */
function getSearchBoxDefaultState(searchQuery: string[]): {
  advancedToggledDefault: boolean;
  fulltextInputDefault: string;
  advancedInputDefault: FormDataEntry[];
} {
  let advancedToggledDefault = true;
  let fulltextInputDefault = '';
  let advancedInputDefault: FormDataEntry[] = [];

  if (
    searchQuery.length == 1 &&
    !searchQuery[0].includes(urlSearchFieldDelimiter)
  ) {
    // Basic/Fulltext Search
    fulltextInputDefault = searchQuery[0];
    advancedToggledDefault = false;
    advancedInputDefault = [{ topicName: null, value: '', mode: 'contains' }];
  } else {
    // Advanced Search
    for (const query of searchQuery) {
      advancedInputDefault.push(parseQueryTopicParams(query));
    }
    // Handle special cases
    if (advancedInputDefault.length === 0) {
      // No URL parameters, default to empty fulltext search
      advancedToggledDefault = false;
      advancedInputDefault = [{ topicName: null, value: '', mode: 'contains' }];
    }
  }

  return { advancedToggledDefault, fulltextInputDefault, advancedInputDefault };
}

export default function SearchBox({
  searchQuery,
  filter,
}: {
  searchQuery: string[];
  filter?: Filter;
}) {
  const { advancedToggledDefault, fulltextInputDefault, advancedInputDefault } =
    getSearchBoxDefaultState(searchQuery);

  const [advancedToggled, setAdvancedToggled] = useState(
    advancedToggledDefault,
  );
  const [fulltextInput, setfulltextInput] = useState(fulltextInputDefault);
  const [advancedInput, setAdvancedInput] = useState(advancedInputDefault);

  const [filterState, setFilterState] = useState<Filter>({
    sources: filter?.sources || AVAILABLE_SOURCES.map((source) => source.name),
    onlyImages: filter?.onlyImages || false,
  });

  let filterContext = useContext(FilterContext);

  // The filter context is either initialized for the search page, or needs to be initialized only for the search box.
  // if the filter context is undefined, it is initialized for the search box.
  if (filterContext == undefined) {
    filterContext = {
      filter: filterState,
      setFilteredSources: (sources: string[]) =>
        setFilterState({ ...filterState, sources: sources }),
      addFilteredSource: (source: string) =>
        setFilterState({
          ...filterState,
          sources: [...filterState.sources, source],
        }),
      removeFilteredSource: (source: string) =>
        setFilterState({
          ...filterState,
          sources: filterState.sources.filter((s) => s !== source),
        }),
      setOnlyImages: (onlyImages: boolean) =>
        setFilterState({ ...filterState, onlyImages: onlyImages }),
      toggleOnlyImages: () =>
        setFilterState({ ...filterState, onlyImages: !filterState.onlyImages }),
    };
  } else {
    filterContext = {
      ...filterContext,
      filter: filterState,
      setFilteredSources: (sources: string[]) =>
        setFilterState({ ...filterState, sources: sources }),
      addFilteredSource: (source: string) =>
        setFilterState({
          ...filterState,
          sources: [...filterState.sources, source],
        }),
      removeFilteredSource: (source: string) =>
        setFilterState({
          ...filterState,
          sources: filterState.sources.filter((s) => s !== source),
        }),
      setOnlyImages: (onlyImages: boolean) =>
        setFilterState({ ...filterState, onlyImages: onlyImages }),
      toggleOnlyImages: () =>
        setFilterState({
          ...filterState,
          onlyImages: !filterState.onlyImages ?? true,
        }),
    };
  }

  return (
    <div className="w-full">
      <FilterContext.Provider
        value={{
          filter: filterState,
          setFilteredSources: filterContext.setFilteredSources,
          addFilteredSource: filterContext.addFilteredSource,
          removeFilteredSource: filterContext.removeFilteredSource,
          setOnlyImages: filterContext.setOnlyImages,
          toggleOnlyImages: filterContext.toggleOnlyImages,
        }}
      >
        <div className="shadow-md bg-white rounded-xl overflow-hidden">
          <SearchSwitch
            advancedToggled={advancedToggled}
            setAdvancedToggled={setAdvancedToggled}
          />
          <div className="overflow-y-auto max-h-[300px]">
            {advancedToggled ? (
              <AdvancedSearch
                input={advancedInput}
                onChangeInput={setAdvancedInput}
              />
            ) : (
              <FulltextSearch
                input={fulltextInput}
                onChangeInput={setfulltextInput}
              />
            )}
          </div>
        </div>
      </FilterContext.Provider>
    </div>
  );
}
