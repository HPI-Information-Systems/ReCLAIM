import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination';
import { FilterContext } from '@/lib/context/FilterContext';
import { Filter } from '@/lib/types/filter';
import { useContext } from 'react';

/**
 * Creates a URL for the given page to navigate to, maintaining the current search query
 * @param toPage Page the link navigates to
 * @param searchQuery Current search query parameters
 * @returns URL to navigate to the given page
 */
function getPaginationHref(
  toPage: number,
  searchQuery: string[],
  filter: Filter | undefined,
) {
  const urlParams = new URLSearchParams();
  searchQuery.forEach((query) => urlParams.append('q', query));
  urlParams.set('page', toPage.toString());
  if (filter) {
    urlParams.set('sources', filter.sources.join(','));
    urlParams.set('onlyImages', filter.onlyImages.toString());
  }
  return '/search?' + urlParams.toString();
}

export default function ResultsPaginator({
  page,
  searchQuery,
  totalPages,
}: {
  page: number;
  searchQuery: string[];
  totalPages: number;
}) {
  const filterContext = useContext(FilterContext);

  return (
    <Pagination className="w-auto m-0 text-highlight-blue">
      <PaginationContent>
        {/* Previous page button */}
        {page > 1 && (
          <PaginationPrevious
            href={getPaginationHref(
              page - 1,
              searchQuery,
              filterContext.filter,
            )}
          />
        )}

        {/* Jump to first page */}
        {page > 2 && (
          <PaginationLink
            href={getPaginationHref(1, searchQuery, filterContext.filter)}
          >
            1
          </PaginationLink>
        )}
        {page > 3 && (
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
        )}

        {/* Previous page number */}
        {page > 1 ? (
          <PaginationLink
            href={getPaginationHref(
              page - 1,
              searchQuery,
              filterContext.filter,
            )}
          >
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
        {page < totalPages && (
          <>
            <PaginationLink
              href={getPaginationHref(
                page + 1,
                searchQuery,
                filterContext.filter,
              )}
            >
              {page + 1}
            </PaginationLink>

            {page + 2 < totalPages && (
              <PaginationItem>
                <PaginationEllipsis />
              </PaginationItem>
            )}

            {page + 1 !== totalPages && (
              <PaginationLink
                href={getPaginationHref(
                  totalPages,
                  searchQuery,
                  filterContext.filter,
                )}
              >
                {totalPages}
              </PaginationLink>
            )}
          </>
        )}

        {/* Next page button */}
        {page < totalPages && (
          <PaginationNext
            href={getPaginationHref(
              page + 1,
              searchQuery,
              filterContext.filter,
            )}
          />
        )}
      </PaginationContent>
    </Pagination>
  );
}
