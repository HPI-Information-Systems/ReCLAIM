import {
  ConfiscationEvent,
  DepositionEvent,
  SupportedSource,
  TransferEvent,
} from '@/lib/client';

const source: SupportedSource = 'wccp';

const event0: ConfiscationEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 0,
  date: {
    raw: {},
    parsed: 'August 1940',
  },
  physical_description: null,
  at_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Alliance Israélite Universelle, Paris',
    },
  },
  from_legal_entity: [
    {
      id: 'bla',
      source_id: source,
      name: {
        raw: {},
        parsed: 'Francis Harburger',
      },
    },
  ] as any,
  from_collection: [
    {
      id: 'bla',
      source_id: source,
      name: {
        raw: {},
        parsed: 'Harburger',
      },
    },
  ],
  by_legal_entity: {
    id: 'bla',
    source_id: source,
    name: {
      raw: {},
      parsed: 'Einsatzstab Reichsleiter Rosenberg',
    },
  },
  with_involvement_of: null,
};

const event1: DepositionEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 1,
  date: {
    raw: {},
    parsed: 'April 1945',
  },
  physical_description: null,
  at_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Hungen',
    },
  },
  deposited_by: null,
  possessor: null,
  depot_number: null,
  collected_in: null,
  with_involvement_of: null,
};

const event2: ConfiscationEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 2,
  date: {
    raw: {},
    parsed: 'August 1940',
  },
  physical_description: null,
  at_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Hungen?',
    },
  },
  from_legal_entity: [
    {
      id: 'bla',
      source_id: source,
      name: {
        raw: {},
        parsed: 'Nazis?',
      },
    },
  ] as any,
  from_collection: null,
  by_legal_entity: {
    id: 'bla',
    source_id: source,
    name: {
      raw: {},
      parsed: 'Allied Forces?',
    },
  },
  with_involvement_of: null,
};

const event3: DepositionEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 3,
  date: {
    raw: {},
    parsed: 'Keine Ahnung',
  },
  physical_description: null,
  at_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Offenbach Archival Depot',
    },
  },
  deposited_by: null,
  possessor: null,
  depot_number: null,
  collected_in: null,
  with_involvement_of: null,
};

const event4: TransferEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 4,
  date: null,
  departure_date: null,
  arrival_date: {
    raw: {},
    parsed: '21. February 1946',
  },
  to_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Wiesbaden Central Collection Point',
    },
  },
  from_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Offenbach Archival Depot',
    },
  },
  by_legal_entity: null,
  identified_by: null,
  possessor_before: null,
  possessor_after: null,
  physical_description: null,
  physical_description_before: null,
  physical_description_after: {
    raw: {},
    parsed: 'bad\nundamaged; A hole in the canvas.',
  },
  with_involvement_of: null,
};

const event5: DepositionEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 5,
  date: {
    raw: {},
    parsed: '21. February 1946',
  },
  physical_description: {
    raw: {},
    parsed: 'bad\nundamaged; A hole in the canvas.',
  },
  at_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Wiesbaden Central Collection Point',
    },
  },
  deposited_by: null,
  possessor: null,
  depot_number: null,
  collected_in: null,
  with_involvement_of: null,
};

const event6: TransferEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 6,
  date: null,
  departure_date: {
    raw: {},
    parsed: '4. July 1951',
  },
  arrival_date: {
    raw: {},
    parsed: '5. July 1951',
  },
  to_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Nürnberg',
    },
  },
  from_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Wiesbaden Central Collection Point',
    },
  },
  by_legal_entity: null,
  identified_by: null,
  possessor_before: null,
  possessor_after: [
    {
      id: 'bla',
      source_id: source,
      name: {
        raw: {},
        parsed: 'JRSO (Jewish Restitution Successor Organization)',
      },
    },
  ] as any,
  physical_description: null,
  physical_description_before: null,
  physical_description_after: null,
  with_involvement_of: null,
};

const event7: DepositionEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 7,
  date: {
    raw: {},
    parsed: '5. July 1951',
  },
  physical_description: null,
  at_location: null,
  deposited_by: null,
  possessor: [
    {
      id: 'bla',
      source_id: source,
      name: {
        raw: {},
        parsed: 'JRSO (Jewish Restitution Successor Organization)',
      },
    },
  ] as any,
  depot_number: null,
  collected_in: null,
  with_involvement_of: null,
};

const event8: TransferEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 8,
  date: null,
  departure_date: {
    raw: {},
    parsed: '1952',
  },
  arrival_date: {
    raw: {},
    parsed: '1952',
  },
  to_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Bezalel National Museum, Jerusalem',
    },
  },
  from_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'JRSO (Jewish Restitution Successor Organization)',
    },
  },
  by_legal_entity: null,
  identified_by: null,
  possessor_before: null,
  possessor_after: null,
  physical_description: null,
  physical_description_before: null,
  physical_description_after: null,
  with_involvement_of: null,
};

const event9: DepositionEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 9,
  date: {
    raw: {},
    parsed: '1952',
  },
  physical_description: null,
  at_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Bezalel National Museum, Jerusalem',
    },
  },
  deposited_by: null,
  possessor: null,
  depot_number: null,
  collected_in: null,
  with_involvement_of: null,
};

const event10: TransferEvent = {
  id: 'bla',
  source_id: source,
  relative_order: 10,
  date: null,
  departure_date: {
    raw: {},
    parsed: '1962',
  },
  arrival_date: null,
  to_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Paris',
    },
  },
  from_location: {
    id: 'bla',
    source_id: source,
    description: {
      raw: {},
      parsed: 'Bezalel National Museum, Jerusalem',
    },
  },
  by_legal_entity: null,
  identified_by: null,
  possessor_before: null,
  possessor_after: [
    {
      id: 'bla',
      source_id: source,
      name: {
        raw: {},
        parsed: 'Francis Harburger',
      },
    },
  ] as any,
  physical_description: null,
  physical_description_before: null,
  physical_description_after: null,
  with_involvement_of: null,
};

export const prep_timeline_data = [
  event0,
  event1,
  event2,
  event3,
  event4,
  event5,
  event6,
  event7,
  event8,
  event9,
  event10,
];
