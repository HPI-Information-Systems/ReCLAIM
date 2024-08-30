import { Header } from '@/components/general/header';
import SearchBox from '@/components/search/searchBox';
import ResultsBox from '@/components/search/searchResults/resultsBox';
import { apiClient } from '@/lib/api/client';
import { CulturalAsset, KunstgraphClient } from '@/lib/client';
import { AVAILABLE_SOURCES } from '@/lib/config/sources';
import { FilterContext } from '@/lib/context/FilterContext';
import { TopicContext } from '@/lib/context/TopicContext';
import { Filter } from '@/lib/types/filter';
import { GetServerSidePropsContext } from 'next';
import { useContext, useEffect, useState } from 'react';

// This controls globally how many assets are displayed on each search results page
const assetsPerPage = 20;

// We use a pipe character as delimiter, so that it is unlikely to be part of a search query
// This is used to separate the different parts of a search query, e.g. "Cultural Asset Title" + delimiter + "search term"
// Must be the same as in the backend
export const urlSearchFieldDelimiter = '|';

export default function SearchPage({
  searchResults,
  searchQuery,
  page,
  totalPages,
  topics,
  filter,
  countOfAssetsMatchingAllFilters,
  countOfAssetsMatchingSomeFilters,
}: {
  searchResults: CulturalAsset[];
  searchQuery: string[];
  page: number;
  totalPages: number;
  topics: Record<string, string>;
  filter?: Filter;
  countOfAssetsMatchingAllFilters: number;
  countOfAssetsMatchingSomeFilters: number;
}) {
  const { setTopics } = useContext(TopicContext);

  if (!filter) {
    filter = {
      sources: AVAILABLE_SOURCES.map((source) => source.name),
      onlyImages: false,
    };
  }

  if (!filter.sources || filter.sources.length === 0) {
    filter.sources = AVAILABLE_SOURCES.map((source) => source.name);
  }

  const [filterState, setFilterState] = useState<Filter>(filter);

  useEffect(() => {
    setFilterState(filter);
  }, [filter]);

  useEffect(() => {
    setTopics(new Map<string, string>(Object.entries(topics)));
  }, []);

  return (
    <>
      <Header logoOverflowHidden={true} />
      <FilterContext.Provider
        value={{
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
        }}
      >
        <div className="mt-10 container">
          <SearchBox searchQuery={searchQuery} filter={filter} />
        </div>
        <ResultsBox
          assets={searchResults}
          searchQuery={searchQuery}
          page={page}
          totalPages={totalPages}
          countOfAssetsMatchingAllFilters={countOfAssetsMatchingAllFilters}
          countOfAssetsMatchingSomeFilters={countOfAssetsMatchingSomeFilters}
          assetsPerPage={assetsPerPage}
        />
      </FilterContext.Provider>
    </>
  );
}

export const getServerSideProps = async ({
  query,
}: GetServerSidePropsContext) => {
  let queryList: string | string[];

  if (!query.q) queryList = '';
  else queryList = query.q;

  const pageNumber = (query.page as string | undefined) ?? '1';

  const sources = query.sources as string | undefined;

  let sourceFilters: string[] = [];
  if (sources) {
    sourceFilters = sources.split(',');
  }
  const onlyWithImages = query.onlyImages as string | undefined;

  let parsedPageNumber = parseInt(pageNumber);
  if (isNaN(parsedPageNumber) || parsedPageNumber < 1) {
    parsedPageNumber = 1;
  }

  const client = apiClient as KunstgraphClient;

  if (typeof queryList === 'string') queryList = [queryList];

  const searchResults =
    await client.culturalAsset.fulltextSearchCulturalAssetSearchGet({
      q: queryList,
      limit: assetsPerPage,
      cursor: assetsPerPage * (parsedPageNumber - 1),
      sources: sourceFilters,
      onlyWithImages: onlyWithImages === 'true',
    });

  const topics = await client.culturalAsset.getTopicsCulturalAssetTopicsGet();

  const total_results_count =
    searchResults.total_count_match_all_search_filters +
    searchResults.total_count_match_some_search_filters;

  return {
    props: {
      searchResults: [
        ...searchResults.results_match_all_search_filters,
        ...searchResults.results_match_some_search_filters,
      ],
      searchQuery: queryList,
      filter: {
        sources: sourceFilters,
        onlyImages: onlyWithImages == 'true',
      },
      page: parsedPageNumber,
      totalPages: Math.ceil(total_results_count / assetsPerPage),
      countOfAssetsMatchingAllFilters:
        searchResults.total_count_match_all_search_filters,
      countOfAssetsMatchingSomeFilters:
        searchResults.total_count_match_some_search_filters,
      topics: topics,
    },
  };
};
