import { culturalAssetProperties } from '../culturalAsset/properties';
import { personProperties } from '../person/properties';
import { collectionProperties } from '../collection/properties';
import { EntryType, PageEntityType } from './types';

export function getEntityProperties(entityType: PageEntityType) {
  let entityProperties: Record<string, { label: string; type: EntryType }> = {};
  if (entityType === PageEntityType.CULTURAL_ASSET) {
    entityProperties = culturalAssetProperties;
  } else if (entityType === PageEntityType.PERSON) {
    entityProperties = personProperties;
  } else if (entityType === PageEntityType.COLLECTION) {
    entityProperties = collectionProperties;
  } else {
    throw new Error(
      'This PageEntityType does not have a property dictionary yet',
    );
  }
  return entityProperties;
}
