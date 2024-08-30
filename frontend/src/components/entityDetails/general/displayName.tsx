import {
  Classification,
  Collection,
  CulturalAsset,
  Location,
  Material,
  Person,
} from '@/lib/client';
import { PageEntityType } from './types';

export function displayNameCulturalAsset(
  culturalAsset: CulturalAsset,
): DisplayAttribute {
  // ideally, display the title of the cultural asset
  if (culturalAsset.title && culturalAsset.title.parsed !== '') {
    return {
      raw: culturalAsset.title.raw,
      parsed: culturalAsset.title.parsed,
    };
  }
  // alternatively, display a identifier of one of the CCPs/sources
  else if (
    culturalAsset.wccp_number &&
    culturalAsset.wccp_number.parsed !== ''
  ) {
    return {
      raw: culturalAsset.wccp_number.raw,
      parsed: 'Wiesbaden No.: ' + culturalAsset.wccp_number.parsed,
    };
  } else if (
    culturalAsset.marburg_number &&
    culturalAsset.marburg_number.parsed !== ''
  ) {
    return {
      raw: culturalAsset.marburg_number.raw,
      parsed: 'Marburg No.: ' + culturalAsset.marburg_number.parsed,
    };
  } else if (
    culturalAsset.munich_number &&
    culturalAsset.munich_number.parsed !== ''
  ) {
    return {
      raw: culturalAsset.munich_number.raw,
      parsed: 'Munich No.: ' + culturalAsset.munich_number.parsed,
    };
  } else if (
    culturalAsset.linz_number &&
    culturalAsset.linz_number.parsed !== ''
  ) {
    return {
      raw: culturalAsset.linz_number.raw,
      parsed: 'Linz No.: ' + culturalAsset.linz_number.parsed,
    };
  } else if (
    culturalAsset.err_number &&
    culturalAsset.err_number.parsed !== ''
  ) {
    return {
      raw: culturalAsset.err_number.raw,
      parsed: 'ERR No.: ' + culturalAsset.err_number.parsed,
    };
  } else if (
    culturalAsset.measurements &&
    culturalAsset.measurements.parsed !== ''
  ) {
    return {
      raw: culturalAsset.measurements.raw,
      parsed: 'Measurements: ' + culturalAsset.measurements.parsed,
    };
  }

  // if everything else fails, display the internal ID
  else {
    return {
      raw: null,
      parsed: 'ID: ' + culturalAsset.id,
    };
  }
}

export function displayNamePerson(person: Person): DisplayAttribute {
  // ideally, display the pseudonym of the person, because in case they have an artist name, it is more likely to be known
  if (person.pseudonym) {
    return {
      raw: person.pseudonym.raw,
      parsed: person.pseudonym.parsed,
    };
  }

  // alternatively, display as much of their name as possible
  else if (person.first_name && person.last_name) {
    return {
      raw: { ...person.first_name.raw, ...person.last_name.raw },
      parsed: person.first_name.parsed + ' ' + person.last_name.parsed,
    };
  } else if (person.name) {
    return {
      raw: person.name.raw,
      parsed: person.name.parsed,
    };
  } else if (person.last_name) {
    return {
      raw: person.last_name.raw,
      parsed: person.last_name.parsed,
    };
  } else if (person.first_name) {
    return {
      raw: person.first_name.raw,
      parsed: person.first_name.parsed,
    };
  }

  // if everything else fails, display the internal ID
  else {
    return { raw: null, parsed: 'ID: ' + person.id };
  }
}

export type DisplayAttribute = {
  raw: Record<string, string> | (Record<string, string> | null)[] | null;
  parsed: string;
};

export function displayNameClassification(
  classification: Classification[],
): DisplayAttribute {
  const raw: (Record<string, string> | null)[] = [];
  const parsed: string[] = [];
  classification.forEach((c) => {
    if (c.name) {
      raw.push(c.name.raw);
      parsed.push(c.name.parsed);
    } else {
      raw.push(null);
      parsed.push('ID: ' + c.id);
    }
  });
  return { raw: raw, parsed: parsed.join(', ') };
}

export function displayNameCollection(
  collection: Collection,
): DisplayAttribute {
  if (collection.name)
    return { raw: collection.name.raw, parsed: collection.name.parsed };
  if (collection.abbreviation)
    return {
      raw: collection.abbreviation.raw,
      parsed: collection.abbreviation.parsed,
    };
  if (collection.description)
    return {
      raw: collection.description.raw,
      parsed: collection.description.parsed,
    };
  return { raw: null, parsed: 'ID: ' + collection.id };
}

export function displayNameMaterial(material: Material[]): DisplayAttribute {
  const raw: (Record<string, string> | null)[] = [];
  const parsed: string[] = [];
  material.forEach((m) => {
    if (m.name) {
      raw.push(m.name.raw);
      parsed.push(m.name.parsed);
    } else {
      raw.push(null);
      parsed.push('ID: ' + m.id);
    }
  });
  return { raw: raw, parsed: parsed.join(', ') };
}

export function displayNameLocation(location: Location): DisplayAttribute {
  if (location.city && location.country) {
    return {
      raw: { ...location.city.raw, ...location.country.raw },
      parsed: location.city.parsed + ', ' + location.country.parsed,
    };
  } else if (location.city) {
    return { raw: location.city.raw, parsed: location.city.parsed };
  } else if (location.region) {
    return {
      raw: location.region.raw,
      parsed: location.region.parsed,
    };
  } else if (location.country) {
    return {
      raw: location.country.raw,
      parsed: location.country.parsed,
    };
  } else if (location.street) {
    return {
      raw: location.street.raw,
      parsed: location.street.parsed,
    };
  } else if (location.description) {
    return {
      raw: location.description.raw,
      parsed: location.description.parsed,
    };
  } else {
    return { raw: null, parsed: 'ID: ' + location.id };
  }
}

export function getRelationDisplayName(
  entityRelation: any,
  label: string,
): DisplayAttribute | null {
  // This function is used to get the display name of a relation of an entity

  if (!entityRelation) return null;

  switch (label) {
    case 'Collection':
      return displayNameCollection(entityRelation);
    case 'Classification':
      return displayNameClassification(entityRelation);
    case 'Material':
      return displayNameMaterial(entityRelation);
    case 'Creator':
      return displayNamePerson(entityRelation);
    case 'Owner':
      return displayNamePerson(entityRelation);
    case 'Creation Location':
    case 'Location':
      return displayNameLocation(entityRelation);
    case 'Based in':
      return displayNameLocation(entityRelation);
    default:
      throw new Error('Unknown relation type for Entity relation: ' + label);
  }
}

export function getEntityDisplayName(
  entity: CulturalAsset | Person | Collection,
  entityType: PageEntityType,
): DisplayAttribute {
  let displayName;
  if (entityType === PageEntityType.PERSON) {
    displayName = displayNamePerson(entity);
  } else if (entityType === PageEntityType.CULTURAL_ASSET) {
    displayName = displayNameCulturalAsset(entity);
  } else if (entityType === PageEntityType.COLLECTION) {
    displayName = displayNameCollection(entity);
  } else {
    throw new Error(
      'This PageEntityType does not have an implementation for displayName yet',
    );
  }
  return displayName;
}
