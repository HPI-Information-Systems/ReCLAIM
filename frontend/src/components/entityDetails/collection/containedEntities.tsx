import { CulturalAsset } from '@/lib/client';
import { EntityCarousel } from '../general/entityCarousel';
import { PageEntityType } from '../general/types';

export function EntitiesContainedInCollection({
  containedEntities = [],
}: {
  containedEntities: CulturalAsset[];
}) {
  return (
    <div className="w-full container pt-10 pb-16 shadow-md rounded-lg my-10 px-10">
      <EntityCarousel
        entites={containedEntities}
        entityType={PageEntityType.CULTURAL_ASSET}
        headline="Cultural Assets in Collection"
      />
    </div>
  );
}
