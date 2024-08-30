import { apiClient } from '@/lib/api/client';
import { KunstgraphClient } from '@/lib/client';
import type { NextApiRequest, NextApiResponse } from 'next';

type ResponseData = string[];

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>,
) {
  const client = apiClient as KunstgraphClient;
  const autocompleteSuggestions =
    await client.autocomplete.fetchAutocompleteCompletionsAutocompleteCompletionsGet(
      {
        q: req.query.q as string,
        topic: req.query.topic as string,
      },
    );
  res.status(200).json(autocompleteSuggestions);
}
