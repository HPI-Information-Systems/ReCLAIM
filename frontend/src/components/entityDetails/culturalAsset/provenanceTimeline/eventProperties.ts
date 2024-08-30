import { EntryType } from '../../general/types';

function createEventProperty(
  label: string,
  entityType: EntryType,
  displayAttribute: string | null = null,
) {
  return {
    label,
    entityType,
    displayAttribute,
  };
}

const baseEventProperties = {
  description: createEventProperty('Description', EntryType.ATTRIBUTE),
  date: createEventProperty('Date', EntryType.ATTRIBUTE),
  physical_description: createEventProperty(
    'Physical Description',
    EntryType.ATTRIBUTE,
  ),
  with_involvement_of: createEventProperty(
    'With Involvement of',
    EntryType.RELATION,
    'name',
  ),
};

export const acquisitionEventProperties = {
  ...baseEventProperties,
  acquisition_cost: createEventProperty(
    'Acquisition Cost',
    EntryType.ATTRIBUTE,
  ),
  at_location: createEventProperty(
    'Acquired at',
    EntryType.RELATION,
    'description',
  ),
  from_collection: createEventProperty(
    'Acquired from',
    EntryType.RELATION,
    'name',
  ),
  from_legal_entity: createEventProperty(
    'Acquired from',
    EntryType.RELATION,
    'name',
  ),
  by_legal_entity: createEventProperty(
    'Acquired by',
    EntryType.RELATION,
    'name',
  ),
  through_legal_entity: createEventProperty(
    'Acquired through',
    EntryType.RELATION,
    'name',
  ),
};

export const depositionEventProperties = {
  ...baseEventProperties,
  depot_number: createEventProperty('Depot Number', EntryType.ATTRIBUTE),
  at_location: createEventProperty(
    'Deposited at',
    EntryType.RELATION,
    'description',
  ),
  deposited_by: createEventProperty('Deposited by', EntryType.RELATION, 'name'),
  possessor: createEventProperty('Possessor', EntryType.RELATION, 'name'),
  collected_in: createEventProperty('Collected in', EntryType.RELATION, 'name'),
};

export const transferEventProperties = {
  ...baseEventProperties,
  departure_date: createEventProperty('Departure Date', EntryType.ATTRIBUTE),
  arrival_date: createEventProperty('Arrival Date', EntryType.ATTRIBUTE),
  physical_description_before: createEventProperty(
    'Physical Description Before',
    EntryType.ATTRIBUTE,
  ),
  physical_description_after: createEventProperty(
    'Physical Description After',
    EntryType.ATTRIBUTE,
  ),
  from_location: createEventProperty(
    'Transferred from',
    EntryType.RELATION,
    'description',
  ),
  to_location: createEventProperty(
    'Transferred to',
    EntryType.RELATION,
    'description',
  ),
  from_collection: createEventProperty(
    'Transferred from',
    EntryType.RELATION,
    'name',
  ),
  to_collection: createEventProperty(
    'Transferred to',
    EntryType.RELATION,
    'name',
  ),
  transferred_by: createEventProperty(
    'Transferred by',
    EntryType.RELATION,
    'name',
  ),
  identified_by: createEventProperty(
    'Identified by',
    EntryType.RELATION,
    'name',
  ),
  possessor_before: createEventProperty(
    'Possessor Before',
    EntryType.RELATION,
    'name',
  ),
  possessor_after: createEventProperty(
    'Possessor After',
    EntryType.RELATION,
    'name',
  ),
};

export const confiscationEventProperties = {
  ...baseEventProperties,
  at_location: createEventProperty(
    'Confiscated at',
    EntryType.RELATION,
    'description',
  ),
  by_legal_entity: createEventProperty(
    'Confiscated by',
    EntryType.RELATION,
    'name',
  ),
  from_legal_entity: createEventProperty(
    'Confiscated from',
    EntryType.RELATION,
    'name',
  ),
  from_collection: createEventProperty(
    'Confiscated from',
    EntryType.RELATION,
    'name',
  ),
};

export const restitutionEventProperties = {
  ...baseEventProperties,
  at_location: createEventProperty(
    'Restituted at Location',
    EntryType.RELATION,
    'description',
  ),
  restituted_to_legal_entity: createEventProperty(
    'Restituted to Legal Entity',
    EntryType.RELATION,
    'name',
  ),
};
