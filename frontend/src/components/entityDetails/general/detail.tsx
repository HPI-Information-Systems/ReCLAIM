import {
  culturalAssetHasImages,
  getCulturalAssetImageURLs,
} from '@/components/entityDetails/culturalAsset/images';
import { Collection, CulturalAsset, Person } from '@/lib/client';
import ImageCarousel from '../culturalAsset/imageCarousel';
import { getEntityDisplayName } from './displayName';
import { Information } from './information';
import { SourceContainer, Title } from './leadingInformation';
import { PageEntityType } from './types';

export default function Detail({
  entity,
  entityType,
}: {
  entity: CulturalAsset | Person | Collection;
  entityType: PageEntityType;
}) {
  const displayName = getEntityDisplayName(entity, entityType).parsed;
  return (
    <div className="container w-full shadow-md py-10 rounded-lg mt-10">
      <Title data={displayName} />
      <div className="items-center mt-5 mb-5 w-full">
        <SourceContainer source={entity.source_id} />
      </div>

      <div className="flex flex-col lg:flex-row">
        <div className="grid lg:grid-cols-3 relative">
          <div className="col-span-2">
            <div className="grid grid-cols-2 w-full lg:mr-10 ml-2">
              <Information entityType={entityType} entity={entity} />
            </div>
          </div>

          {entityType === PageEntityType.CULTURAL_ASSET && (
            <div className="col-span-1 ml-5">
              <div className="w-full lg:mt-2 lg:sticky lg:top-0">
                {culturalAssetHasImages(entity) && (
                  <ImageCarousel
                    title={displayName}
                    imgURLs={getCulturalAssetImageURLs(entity)}
                  />
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
