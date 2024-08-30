import { apiClient } from '@/lib/api/client';

import { GetServerSideProps } from 'next';

import Detail from '@/components/entityDetails/general/detail';
import { Title } from '@/components/entityDetails/general/leadingInformation';
import { PageEntityType } from '@/components/entityDetails/general/types';
import { Header } from '@/components/general/header';
import { ResultList } from '@/components/search/searchResults/resultsBox';
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination';
import { Collection, CulturalAsset } from '@/lib/client';

type CollectionPageProps = {
  collection: Collection;
  assetsInCollection: CulturalAsset[];
  page: number;
  numberOfPages: number;
  numberOfResults?: number;
};

export default function CollectionPage({
  collection,
  assetsInCollection,
  page,
  numberOfPages,
  numberOfResults,
}: CollectionPageProps) {
  function getPaginationHref(page: number) {
    const collection_id = collection.id;
    return `/collection/${collection_id}?page=${page}`;
  }

  return (
    <>
      <Header logoOverflowHidden={true} />
      <div className="container flex flex-col w-full h-full">
        <Detail
          entity={{ ...collection }}
          entityType={PageEntityType.COLLECTION}
        />

        <div className="flex flex-col mt-10 mb-5">
          <Title
            data={`Showing ${assetsInCollection.length} of ${numberOfResults} assets in this collection.`}
          />
        </div>
        <ResultList
          assets={assetsInCollection}
          startIndex={0}
          numToDisplay={20}
        />

        <Pagination className="ml-auto !justify-end w-full text-highlight-blue my-4">
          <PaginationContent>
            {/* Previous page button */}
            {page > 1 && (
              <PaginationPrevious href={getPaginationHref(page - 1)} />
            )}

            {/* Jump to first page */}
            {page > 2 && (
              <PaginationLink href={getPaginationHref(1)}>1</PaginationLink>
            )}
            {page > 3 && (
              <PaginationItem>
                <PaginationEllipsis />
              </PaginationItem>
            )}

            {/* Previous page number */}
            {page > 1 ? (
              <PaginationLink href={getPaginationHref(page - 1)}>
                {page - 1}
              </PaginationLink>
            ) : (
              <></>
            )}
            {/* Current page number */}
            <PaginationItem>
              <strong>{page}</strong>
            </PaginationItem>
            {/* Next and last page number */}
            {page < numberOfPages && (
              <>
                <PaginationLink href={getPaginationHref(page + 1)}>
                  {page + 1}
                </PaginationLink>

                {page + 2 < numberOfPages && (
                  <PaginationItem>
                    <PaginationEllipsis />
                  </PaginationItem>
                )}

                {page + 1 !== numberOfPages && (
                  <PaginationLink href={getPaginationHref(numberOfPages)}>
                    {numberOfPages}
                  </PaginationLink>
                )}
              </>
            )}

            {/* Next page button */}
            {page < numberOfPages && (
              <PaginationNext href={getPaginationHref(page + 1)} />
            )}
          </PaginationContent>
        </Pagination>
      </div>
    </>
  );
}

export const getServerSideProps: GetServerSideProps<
  CollectionPageProps
> = async (args) => {
  const id = args.params?.id as string;
  const client = apiClient;

  let pageNum = parseInt(args?.query?.page as string);

  if (isNaN(pageNum) || pageNum < 1) {
    pageNum = 1;
  }

  try {
    const collection = await client.collection.getByIdCollectionGetByIdGet({
      id: id,
    });

    const {
      entities: assetsInCollection,
      total_page_count: numberOfPages,
      total_result_count: numberOfResults,
    } = await client.collection.getCulturalAssetsByCollectionIdCollectionGetCulturalAssetsByCollectionIdGet(
      {
        id: id,
        page: pageNum,
      },
    );

    return {
      props: {
        collection,
        assetsInCollection,
        page: pageNum,
        numberOfPages,
        numberOfResults,
      },
    };
  } catch (error) {
    console.log(error);
    return {
      notFound: true,
    };
  }
};
