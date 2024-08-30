import { EntryType } from '../general/types';

export const collectionProperties = {
  name: { label: 'Name', type: EntryType.ATTRIBUTE },
  abbreviation: { label: 'Abbreviation', type: EntryType.ATTRIBUTE },
  description: { label: 'Description', type: EntryType.ATTRIBUTE },
  owned_by: { label: 'Owner', type: EntryType.RELATION_WITH_LINK },
};
