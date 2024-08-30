import { EntryType } from '../general/types';

// Keep this updated with Person
// Order of the keys is the order in which they are displayed
export const personProperties = {
  first_name: { label: 'First Name', type: EntryType.ATTRIBUTE },
  last_name: { label: 'Last Name', type: EntryType.ATTRIBUTE },
  name: { label: 'Name', type: EntryType.ATTRIBUTE },
  pseudonym: { label: 'Pseudonym', type: EntryType.ATTRIBUTE },
  lifetime: { label: 'Lifetime', type: EntryType.ATTRIBUTE },
  history_description: {
    label: 'History Description',
    type: EntryType.ATTRIBUTE,
  },
  birth_date: {
    label: 'Birth Date',
    type: EntryType.ATTRIBUTE,
  },
  structured_birth_date: {
    label: 'Structured Birth Date',
    type: EntryType.ATTRIBUTE,
  },
  death_date: { label: 'Death Date', type: EntryType.ATTRIBUTE },
  structured_death_date: {
    label: 'Structured Death Date',
    type: EntryType.ATTRIBUTE,
  },

  born_in_location: { label: 'Born in Location', type: EntryType.RELATION },
  died_in_location: { label: 'Died in Location', type: EntryType.RELATION },
  based_in: { label: 'Based in', type: EntryType.RELATION },
  archival_source_description: {
    label: 'Archival Source Description',
    type: EntryType.ATTRIBUTE,
  },
} as const;
