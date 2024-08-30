import { FormDataEntry } from '@/components/search/searchBox';
import { urlSearchFieldDelimiter } from '@/pages/search';
import { Filter } from '../types/filter';

/**
 * Creates a URL for the given fulltext search query to navigate to
 * @param input The text input of the user to search for
 * @param page The page number to be retrieved
 * @returns Parsed URL for the given fulltext search query to navigate to
 */
export function useFulltextSearchQuery(
  input: string,
  filter?: Filter,
  page: number = 1,
) {
  console.log(input);
  const queryParams = new URLSearchParams();
  queryParams.append('q', input);
  queryParams.append('page', page.toString());
  if (filter) {
    queryParams.set('sources', filter.sources.join(','));
    queryParams.set('onlyImages', filter.onlyImages.toString());
  }
  return '/search?' + queryParams.toString();
}

/**
 * Generates a URL query from the advanced search input
 * @param input Advanced search form data entries
 * @param page Page to navigate to
 * @returns The /search URL with the query parameters as a string
 */
export function useAdvancedSearchQuery(
  input: FormDataEntry[],
  filter?: Filter,
  page: number = 1,
) {
  if (advancedSearchInputValid(input) === false) {
    return '';
  }
  const queryParams = new URLSearchParams();

  for (const row of input) {
    let query = row.mode === 'contains' ? '' : '!';
    query += row.topicName + urlSearchFieldDelimiter;
    query += row.value;
    queryParams.append('q', query);
  }
  queryParams.set('page', page.toString());
  if (filter) {
    queryParams.set('sources', filter.sources.join(','));
    queryParams.set('onlyImages', filter.onlyImages.toString());
  }
  return '/search?' + queryParams.toString();
}

/**
 * If at least one of the advanced search topics is not specified ('Select topic'), this function returns false
 * @param input Advanced search form data entries
 * @returns Whether all topics are filled in
 */
export function advancedSearchInputValid(input: FormDataEntry[]) {
  return input.every((row) => row.topicName !== null);
}
