import { getEntityDisplayName } from '@/components/entityDetails/general/displayName';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { CulturalAsset, Person, Collection } from '@/lib/client';
import { ImageIcon } from 'lucide-react';
import { Checkbox } from '@/components/ui/checkbox';
import Image from 'next/legacy/image';
import { SquareUserRound } from 'lucide-react';
import Link from 'next/link';
import { culturalAssetHasImages } from '@/components/entityDetails/culturalAsset/images';
import { PageEntityType } from '@/components/entityDetails/general/types';
import { SourceContainer } from '@/components/entityDetails/general/leadingInformation';

function getEntityImagePlaceholder(entityType: PageEntityType) {
  if (
    entityType === PageEntityType.CULTURAL_ASSET ||
    entityType === PageEntityType.COLLECTION // Collection has no individual placeholder yet
  ) {
    return (
      <div className="items-center flex justify-center">
        <ImageIcon
          className={'h-16 w-auto stroke-highlight-blue'}
          strokeWidth={0.75}
        />
      </div>
    );
  } else if (entityType === PageEntityType.PERSON) {
    return (
      <div className="items-center flex justify-center">
        <SquareUserRound
          className={'h-32 w-auto stroke-highlight-blue'}
          strokeWidth={0.75}
        />
      </div>
    );
  }
}

function getAlternativeInformation(entity: CulturalAsset) {
  return (
    <div className="mt-5 -ml-6 font-sans text-black font-sans text-sm space-y-2">
      {entity.wccp_number && entity.wccp_number.parsed !== '' && (
        <p>
          <strong>{'Wiesbaden No.: '}</strong> {entity.wccp_number.parsed}
        </p>
      )}
      {entity.marburg_number && entity.marburg_number.parsed !== '' && (
        <p>
          <strong>{'Marburg No.: '}</strong>
          {entity.marburg_number.parsed}
        </p>
      )}
      {entity.munich_number && entity.munich_number.parsed !== '' && (
        <p>
          <strong>{'Munich No.: '}</strong>
          {entity.munich_number.parsed}
        </p>
      )}
      {entity.linz_number && entity.linz_number.parsed !== '' && (
        <p>
          <strong>{'Linz No.: '}</strong> {entity.linz_number.parsed}
        </p>
      )}
      {entity.err_number && entity.err_number.parsed !== '' && (
        <p>
          <strong>{'ERR No.: '}</strong>
          {entity.err_number.parsed}
        </p>
      )}
      {entity.bundesarchiv_signature &&
        entity.bundesarchiv_signature.parsed !== '' && (
          <p>
            <strong>{'Bundesarchiv Signature: '}</strong>
            {entity.bundesarchiv_signature.parsed}
          </p>
        )}
    </div>
  );
}

/**
 * Returns the URL of the image to be displayed in search result preview for a cultural asset with the priority: depicted_in_image, referenced_in_card_image_front, referenced_in_card_image, referenced_in_card_image_back
 * @param culturalAsset The cultural asset to get the image URL from
 * @returns The URL of the image to be displayed in the search result preview
 */
export function getCulturalAssetPreviewDisplayImageURL(
  culturalAsset: CulturalAsset,
) {
  if (
    culturalAsset.depicted_in_image &&
    culturalAsset.depicted_in_image.length > 0
  ) {
    return culturalAsset.depicted_in_image[0].url;
  }
  if (
    culturalAsset.referenced_in_card_image_front &&
    culturalAsset.referenced_in_card_image_front.length > 0
  ) {
    return culturalAsset.referenced_in_card_image_front[0].url;
  }
  if (
    culturalAsset.referenced_in_card_image &&
    culturalAsset.referenced_in_card_image.length > 0
  ) {
    return culturalAsset.referenced_in_card_image[0].url;
  }
  if (
    culturalAsset.referenced_in_card_image_back &&
    culturalAsset.referenced_in_card_image_back.length > 0
  ) {
    return culturalAsset.referenced_in_card_image_back[0].url;
  }
  return '';
}

export default function ResultPreview({
  entity,
  entityType,
  updateCheckStatus,
  isEntityChecked,
  showCheckbox,
  columnWidth = 250,
}: {
  entity: CulturalAsset | Person | Collection;
  entityType: PageEntityType;
  updateCheckStatus?: (id: string) => void;
  isEntityChecked: boolean;
  showCheckbox: boolean;
  columnWidth?: number;
}) {
  const displayName = getEntityDisplayName(entity, entityType).parsed;

  let typeInURL = '';

  if (entityType === PageEntityType.CULTURAL_ASSET) {
    typeInURL = 'culturalAsset';
  } else if (entityType === PageEntityType.PERSON) {
    typeInURL = 'person';
  } else if (entityType === PageEntityType.COLLECTION) {
    typeInURL = 'collection';
  }

  return (
    <Card className="hover:shadow-xl transition relative">
      {showCheckbox && updateCheckStatus && (
        <div className="absolute top-5 right-5">
          <Checkbox
            id={`check_${entity.id}`}
            isChecked={isEntityChecked}
            checkHandler={() => updateCheckStatus(entity.id)}
          />
        </div>
      )}
      <Link href={`/${typeInURL}/${encodeURIComponent(entity.id)}`}>
        <p className="leading-5 font-semibold text-highlight-blue mt-5 truncate w-[90%]">
          {displayName}
        </p>
        <SourceContainer source={entity.source_id} inPreview={true} />
        <CardContent>
          <div className="h-40 w-full mt-auto relative">
            {entityType === PageEntityType.CULTURAL_ASSET &&
            culturalAssetHasImages(entity) ? (
              <Image
                src={getCulturalAssetPreviewDisplayImageURL(entity)}
                alt={displayName}
                layout="fill"
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                objectFit="contain"
              />
            ) : entityType === PageEntityType.CULTURAL_ASSET ? (
              getAlternativeInformation(entity)
            ) : (
              getEntityImagePlaceholder(entityType)
            )}
          </div>
        </CardContent>
      </Link>
    </Card>
  );
}
