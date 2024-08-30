import { getRelationDisplayName } from './displayName';
import { getCulturalAssetPreviewDisplayImageURL } from '@/components/search/searchResults/resultPreview';
import {
  CulturalAsset,
  Person,
  Collection,
  Entry_str_,
  SupportedSource,
} from '@/lib/client';
import { getSourceName } from '@/lib/hooks/getSourceFromSourceAttribute';
import { PageEntityType, EntryType } from './types';
import React from 'react';
import { getEntityProperties } from './properties';
import { culturalAssetHasImages } from '../culturalAsset/images';

function ImageRow({ similarEntities }: { similarEntities: CulturalAsset[] }) {
  // for now, only Cultural Assets have images
  // Check if the row would be empty
  let rowEmpty = true;
  similarEntities.map((entity) => {
    if (culturalAssetHasImages(entity)) rowEmpty = false;
  });
  if (!rowEmpty) {
    return (
      <>
        <tr className="hover:bg-background-gray/40">
          <td className="align-top font-bold mb-5 mr-5 bg-background-gray border text-left px-2 py-2">
            {'Image'}
          </td>
          {similarEntities.map((similarEntitiy, index) => {
            return (
              <td
                key={index}
                className={`align-top border px-2 py-2 ${index === 0 ? 'bg-background-gray/30' : ''}`}
              >
                <img
                  className="h-32 object-scale-down"
                  src={getCulturalAssetPreviewDisplayImageURL(similarEntitiy)}
                  /*alt="No image"*/
                />
              </td>
            );
          })}
        </tr>
      </>
    );
  } else return null; // do not show image row if it would be empty
}

function SourceRow({ sourceIds }: { sourceIds: SupportedSource[] }) {
  return (
    <>
      <tr className="hover:bg-background-gray/40">
        <td
          className={
            'align-top font-bold mb-5 mr-5 bg-background-gray border text-left px-2 py-2'
          }
        >
          {'Source'}
        </td>
        {sourceIds.map((sourceId, index) => {
          return (
            <td
              key={index}
              className={`align-top border px-2 py-2 ${index === 0 ? 'bg-background-gray/30' : ''}`}
            >
              {getSourceName(sourceId)}
            </td>
          );
        })}
      </tr>
    </>
  );
}

export function TableRow({
  label,
  comparisonData = [], //potentially data from multiple sources
}: {
  label: string;
  comparisonData: (string | null)[];
}) {
  // Check if the row would be empty
  let rowEmpty = true;
  comparisonData.map((data) => {
    if (data !== null) rowEmpty = false;
  });
  if (!rowEmpty) {
    return (
      <>
        <tr className="hover:bg-background-gray/40">
          <td className="align-top font-bold mb-5 mr-5 bg-background-gray border text-left px-2 py-2">
            {label}
          </td>
          {comparisonData.map((data, index) => {
            // data of each source
            if (data === null)
              return (
                <td
                  key={index}
                  className={`border px-2 py-2 ${index === 0 ? 'bg-background-gray/30' : ''}`}
                ></td>
              );
            else
              return (
                <td
                  key={index}
                  className={`align-top border px-2 py-2 ${index === 0 ? 'bg-background-gray/30' : ''}`}
                >
                  {data}
                </td>
              );
          })}
        </tr>
      </>
    );
  } else return null; // skip row if it would be empty
}

export default function ComparisonTable({
  similarEntities = [],
  entityType,
}: {
  similarEntities: CulturalAsset[] | Person[] | Collection[];
  entityType: PageEntityType;
}) {
  const properties = getEntityProperties(entityType);
  return (
    <div className="w-full mt-10">
      <table className="table-auto">
        <tbody>
          {entityType === PageEntityType.CULTURAL_ASSET && (
            <ImageRow similarEntities={similarEntities} />
          )}

          <SourceRow
            sourceIds={similarEntities.map(
              (similarEntities) => similarEntities.source_id,
            )}
          />

          {Object.entries(properties).map(([key, { label, type }], index) => {
            let data: (string | null)[] = [];
            if (type === EntryType.ATTRIBUTE) {
              data = similarEntities.map((similarEntity) => {
                let dataEntry;
                if (entityType === PageEntityType.CULTURAL_ASSET) {
                  dataEntry = (similarEntity as CulturalAsset)[
                    key as keyof CulturalAsset
                  ];
                } else if (entityType === PageEntityType.PERSON) {
                  dataEntry = (similarEntity as Person)[key as keyof Person];
                } else {
                  //dataEntry = (entity as Collection)[property as keyof Collection];
                }
                return (dataEntry as Entry_str_)?.parsed === undefined
                  ? null
                  : (dataEntry as Entry_str_)?.parsed;
              });
            } else if (
              type === EntryType.RELATION ||
              type === EntryType.RELATION_WITH_LINK
            ) {
              data = similarEntities.map((similarEntity) => {
                let entityRelation;
                if (entityType === PageEntityType.CULTURAL_ASSET) {
                  entityRelation = (similarEntity as CulturalAsset)[
                    key as keyof CulturalAsset
                  ];
                } else if (entityType === PageEntityType.PERSON) {
                  entityRelation = (similarEntity as Person)[
                    key as keyof Person
                  ];
                } else if (entityType === PageEntityType.COLLECTION) {
                  entityRelation = (similarEntity as Collection)[
                    key as keyof Collection
                  ];
                }
                return (
                  getRelationDisplayName(entityRelation, label)?.parsed || null
                );
              });
            }
            return <TableRow key={index} label={label} comparisonData={data} />;
          })}
        </tbody>
      </table>
    </div>
  );
}
