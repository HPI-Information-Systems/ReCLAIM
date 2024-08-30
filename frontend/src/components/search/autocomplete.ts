export async function fetchAutocompleteData(query: string, topic_name: string) {
  const response = await fetch(
    `/api/autocomplete?q=${query}&topic=${topic_name}`,
  );
  if (!response.ok) {
    console.error('Autocomplete network response returned an error', response);
  }
  const data: string[] = await response.json();
  return data;
}
