import { KunstgraphClient } from '../client';

export const apiClient = new KunstgraphClient({
  BASE:
    process.env.API_BASE_URL ||
    'http://vm-bp2024fn1.cloud.dhclab.i.hpi.de:8000',
});
