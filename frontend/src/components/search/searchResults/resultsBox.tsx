import { PageEntityType } from '@/components/entityDetails/general/types';
import { CulturalAsset } from '@/lib/client';
import { useEffect, useRef, useState } from 'react';
import ResultsPaginator from './resultPaginator';
import ResultPreview from './resultPreview';

export function ResultList({
  assets,
  startIndex,
  numToDisplay,
}: {
  assets: CulturalAsset[];
  startIndex: number;
  numToDisplay: number;
}) {
  const gridContainerRef = useRef<HTMLUListElement>(null);

  const [columnWidth, setColumnWidth] = useState<number>(0);

  useEffect(() => {
    function handleResize() {
      if (gridContainerRef.current) {
        const gridStyle = window.getComputedStyle(gridContainerRef.current);
        const columnCount = parseInt(
          gridStyle
            .getPropertyValue('grid-template-columns')
            .split(' ')
            .length.toString(),
          10,
        );
        const containerWidth = gridContainerRef.current.clientWidth;
        const calculatedColumnWidth = containerWidth / columnCount;
        setColumnWidth(calculatedColumnWidth);
      }
    }

    window.addEventListener('resize', handleResize);
    handleResize();

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const assetsToDisplay = [];
  for (let i = startIndex; i < startIndex + numToDisplay; i++) {
    if (i >= assets.length) {
      break;
    }

    assetsToDisplay.push(
      <li key={assets[i].id} className="flex-1 basis-48">
        <ResultPreview
          entity={assets[i]}
          entityType={PageEntityType.CULTURAL_ASSET}
          isEntityChecked={false}
          showCheckbox={false}
          columnWidth={columnWidth}
        />
      </li>,
    );
  }

  return (
    <>
      {assetsToDisplay.length === 0 ? (
        <p className="mt-5">No results were found for the given query.</p>
      ) : (
        <ul
          ref={gridContainerRef}
          className="w-full gap-4 h-full grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 grid-flow-row-dense"
        >
          {assetsToDisplay}
        </ul>
      )}
    </>
  );
}

export default function ResultsBox({
  assets,
  searchQuery,
  page,
  totalPages,
  countOfAssetsMatchingAllFilters,
  countOfAssetsMatchingSomeFilters,
  assetsPerPage,
}: {
  assets: CulturalAsset[];
  searchQuery: string[];
  page: number;
  totalPages: number;
  countOfAssetsMatchingAllFilters: number;
  countOfAssetsMatchingSomeFilters: number;
  assetsPerPage: number;
}) {
  if (assets.length === 0) {
    return (
      <div className="container overflow-hidden mx-auto bg-white my-20">
        <h1 className="text-3xl grow text-highlight-blue">Search Results</h1>
        <p className="mt-5">No results were found for the given query.</p>
      </div>
    );
  }

  const numPagesMatchingAllSearchFilters = Math.ceil(
    countOfAssetsMatchingAllFilters / assetsPerPage,
  );

  // Base case: all assets on this match all categories
  let numCulturalAssetsMatchingAllSearchFiltersOnPage = assets.length;

  // When some assets match all catgeories and some assets match only some categories
  if (page * assetsPerPage - countOfAssetsMatchingAllFilters > 0) {
    numCulturalAssetsMatchingAllSearchFiltersOnPage =
      assetsPerPage - (page * assetsPerPage - countOfAssetsMatchingAllFilters);
  }

  // When all assets match only some categories
  if (page * assetsPerPage - countOfAssetsMatchingAllFilters >= assetsPerPage) {
    numCulturalAssetsMatchingAllSearchFiltersOnPage = 0;
  }

  const matchingAllAndSomeVisible =
    numCulturalAssetsMatchingAllSearchFiltersOnPage !== 0 &&
    numCulturalAssetsMatchingAllSearchFiltersOnPage !== assets.length;

  return (
    <div className="container overflow-hidden mx-auto bg-white my-20">
      <div className="w-full flex flex-row items-center justify-center mb-10">
        <h1 className="text-3xl grow text-highlight-blue">
          {page <= numPagesMatchingAllSearchFilters
            ? searchQuery.length === 1
              ? countOfAssetsMatchingAllFilters === 1
                ? '1 Result'
                : `${countOfAssetsMatchingAllFilters} Results`
              : countOfAssetsMatchingAllFilters === 1
                ? '1 Result Matching All Categories'
                : `${countOfAssetsMatchingAllFilters} Results Matching All Categories`
            : countOfAssetsMatchingSomeFilters === 1
              ? '1 Result Matching Only Some Categories'
              : `${countOfAssetsMatchingSomeFilters} Results Matching Only Some Categories`}
        </h1>
        <ResultsPaginator
          searchQuery={searchQuery}
          page={page}
          totalPages={totalPages}
        />
      </div>
      <ResultList
        assets={assets}
        startIndex={0}
        numToDisplay={
          numCulturalAssetsMatchingAllSearchFiltersOnPage > 0
            ? numCulturalAssetsMatchingAllSearchFiltersOnPage
            : assets.length
        }
      />
      {matchingAllAndSomeVisible && (
        <div>
          <h1 className="text-3xl grow text-highlight-blue my-10">
            {countOfAssetsMatchingSomeFilters === 1
              ? '1 Result Matching Only Some Categories'
              : `${countOfAssetsMatchingSomeFilters} Results Matching Only Some Categories`}
          </h1>
          <ResultList
            assets={assets}
            startIndex={numCulturalAssetsMatchingAllSearchFiltersOnPage}
            numToDisplay={
              assets.length - numCulturalAssetsMatchingAllSearchFiltersOnPage
            }
          />
        </div>
      )}
      <div className="mt-5 flex justify-end">
        <ResultsPaginator
          searchQuery={searchQuery}
          page={page}
          totalPages={totalPages}
        />
      </div>
    </div>
  );
}
