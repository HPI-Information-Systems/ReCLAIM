import { Collection, CulturalAsset } from '@/lib/client';
import { EntityCarousel } from '../general/entityCarousel';
import { PageEntityType } from '../general/types';

export default function RelatedEntities({
  createdCulturalAssets = [], // Provide a default value for assets, otherwise it will be undefined and the build process will fail
  ownedCulturalAssets = [],
  ownedCollections = [],
}: {
  createdCulturalAssets: CulturalAsset[];
  ownedCulturalAssets: CulturalAsset[];
  ownedCollections: Collection[];
}) {
  return (
    <div className="w-full container pt-10 pb-16 shadow-md rounded-lg my-10 px-10">
      <EntityCarousel
        entites={createdCulturalAssets}
        entityType={PageEntityType.CULTURAL_ASSET}
        headline="Created Cultural Assets"
      />
      <EntityCarousel
        entites={ownedCulturalAssets}
        entityType={PageEntityType.CULTURAL_ASSET}
        headline="Owned Cultural Assets"
      />
      <EntityCarousel
        entites={ownedCollections}
        entityType={PageEntityType.COLLECTION}
        headline="Owned Collections"
      />
    </div>
  );
}
