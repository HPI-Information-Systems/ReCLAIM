import React from 'react';
import { CulturalAsset, Person, Collection } from '@/lib/client';
import { ExportButton } from '../../general/tooltip';
import { CSVLink } from 'react-csv';
import { getSourceName } from '@/lib/hooks/getSourceFromSourceAttribute';
import { Download } from 'lucide-react';
import { getRawParsedDataForEachProperty } from './information';
import { getEntityProperties } from './properties';
import { getCulturalAssetImageURLs } from '../culturalAsset/images';
import { PageEntityType } from './types';

function formatHeadersForCSV(entityType: PageEntityType) {
  const prefixArray = [
    { label: 'ID', key: 'id' },
    { label: 'Source', key: 'source' },
    { label: 'Image URL(s)', key: 'image_urls' },
  ];
  const entityProperties = getEntityProperties(entityType);
  const array = prefixArray.concat(
    Object.entries(entityProperties).flatMap(([key, { label }]) => [
      { label, key },
      { label: 'Unprocessed ' + label, key: 'raw_' + key },
    ]),
  );
  return array;
}

function formatDataForCSV(
  entity: CulturalAsset | Person | Collection,
  entityType: PageEntityType,
) {
  const parsedData: Record<string, any> = {};
  const rawData: Record<string, any> = {};

  getRawParsedDataForEachProperty(
    entity,
    entityType,
    (property, parsedValue, rawValue, _, __) => {
      parsedData[property] = parsedValue;
      rawData[property] = rawValue;
    },
  );

  //remove Object substructure from rawData (Object.values returns an array of the values of the object, always containing only one value)
  Object.keys(rawData).forEach((key) => {
    rawData[key] = Object.values(rawData[key])[0];
  });
  //classifications and materials contain another Object substructure, so we need to convert them to an array
  if (rawData['classified_as']) {
    rawData['classified_as'] = Object.values(rawData['classified_as']);
  }
  if (rawData['consists_of_material']) {
    rawData['consists_of_material'] = Object.values(
      rawData['consists_of_material'],
    );
  }

  //add the prefix raw_ to the keys of rawData and remove Object substructure
  Object.keys(rawData).forEach((key) => {
    rawData['raw_' + key] = rawData[key];
    delete rawData[key];
  });

  // return source, image urls, parsed data and raw data as one object
  return [
    {
      id: entity.id,
      source: getSourceName(entity.source_id),
      image_urls:
        entityType === PageEntityType.CULTURAL_ASSET
          ? getCulturalAssetImageURLs(entity)
          : [],
      ...parsedData,
      ...rawData,
    },
  ];
}

function CSVLinkContainer({
  csvData,
  filename,
  entityType,
}: {
  csvData: any;
  filename: string;
  entityType: PageEntityType;
}): JSX.Element {
  return (
    <CSVLink
      data={csvData}
      headers={formatHeadersForCSV(entityType)}
      filename={filename}
      separator=";"
    >
      <div>
        <Download />
      </div>
    </CSVLink>
  );
}

export default function CSVExport({
  currentEntity,
  similarEntities = [], // Provide a default value for assets, otherwise it will be undefined and the build process will fail
  entitiesCheckedStatus,
  entityType,
}: {
  currentEntity: CulturalAsset | Person | Collection;
  similarEntities: CulturalAsset[] | Person[] | Collection[];
  entitiesCheckedStatus: { [key: string]: boolean };
  entityType: PageEntityType;
}) {
  return (
    <div className="mt-5 ml-3">
      <ExportButton
        csvLink={CSVLinkContainer({
          csvData: formatDataForCSV(currentEntity, entityType).concat(
            similarEntities
              .filter(
                (similarEntity) => entitiesCheckedStatus[similarEntity.id],
              )
              .map((similarEntity) =>
                formatDataForCSV(similarEntity, entityType),
              )
              .flat(), // flat() is used to remove subarray structure
          ),
          filename:
            currentEntity.id +
            '_' +
            similarEntities
              .filter(
                (similarEntity) => entitiesCheckedStatus[similarEntity.id],
              )
              .map((similarEntity) => similarEntity.id)
              .join('_') +
            '.csv',
          entityType: entityType,
        })}
      />
    </div>
  );
}
