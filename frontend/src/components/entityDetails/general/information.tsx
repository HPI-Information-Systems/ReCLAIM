import { CulturalAsset, Person, Collection, Entry_str_ } from '@/lib/client';
import { TooltipRow } from '../../general/tooltip';
import { getRelationDisplayName } from './displayName';
import { PageEntityType, EntryType } from './types';
import { getEntityProperties } from './properties';

export function getRawParsedDataForEachProperty(
  entity: CulturalAsset | Person | Collection,
  entityType: PageEntityType,
  callback: (
    property: string,
    parsedData: string,
    rawData: Record<string, string> | (Record<string, string> | null)[] | null,
    attributeLabel: string,
    attributeType: EntryType,
  ) => any,
) {
  const entityProperties = getEntityProperties(entityType);

  return Object.entries(entityProperties).map(([property, { label, type }]) => {
    let dataEntry;
    if (entityType === PageEntityType.CULTURAL_ASSET) {
      dataEntry = (entity as CulturalAsset)[property as keyof CulturalAsset];
    } else if (entityType === PageEntityType.PERSON) {
      dataEntry = (entity as Person)[property as keyof Person];
    } else if (entityType === PageEntityType.COLLECTION) {
      dataEntry = (entity as Collection)[property as keyof Collection];
    }

    // Check if the property is present in the entity, otherwise skip
    if (dataEntry === null) return null;

    let parsedData = '';
    let rawData = null;
    if (type === EntryType.ATTRIBUTE) {
      parsedData = (dataEntry as Entry_str_)?.parsed || '';
      rawData = (dataEntry as Entry_str_)?.raw || null;
    } else if (
      type === EntryType.RELATION ||
      type === EntryType.RELATION_WITH_LINK
    ) {
      const relationData = getRelationDisplayName(dataEntry, label);
      if (relationData) {
        parsedData = relationData.parsed;
        rawData = relationData.raw || null;
      }
    }
    return callback(property, parsedData, rawData, label, type);
  });
}

export function Information({
  entity,
  entityType,
}: {
  entity: CulturalAsset | Person | Collection;
  entityType: PageEntityType;
}) {
  function getRelatedEntityLink(propertyType: EntryType, property: string) {
    if (propertyType !== EntryType.RELATION_WITH_LINK) return undefined;

    if (entityType === PageEntityType.CULTURAL_ASSET) {
      if (property === 'created_by') {
        return `/person/${(entity as CulturalAsset).created_by?.id || null}`;
      } else if (property === 'collected_in') {
        return `/collection/${(entity as CulturalAsset).collected_in?.id || null}`;
      }
    }

    if (entityType === PageEntityType.COLLECTION) {
      if (property === 'owned_by') {
        return `/person/${(entity as Collection).owned_by?.id || null}`;
      }
    }

    return undefined;
  }

  return (
    <>
      {getRawParsedDataForEachProperty(
        entity,
        entityType,
        (property, parsedValue, rawValue, propertyLabel, propertyType) => {
          return (
            <TooltipRow
              key={property}
              label={propertyLabel}
              data={parsedValue}
              rawData={rawValue}
              link={getRelatedEntityLink(propertyType, property)}
            />
          );
        },
      )}
    </>
  );
}
