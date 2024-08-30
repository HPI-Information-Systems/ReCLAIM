import { apiClient } from '@/lib/api/client';
import {
  CulturalAsset,
  SimilarEntity_CulturalAsset_,
  TransferEvent,
  AcquisitionEvent,
  DepositionEvent,
  ConfiscationEvent,
  RestitutionEvent,
} from '@/lib/client';
import { GetStaticPaths, GetStaticProps } from 'next';

import Detail from '@/components/entityDetails/general/detail';
import { Header } from '@/components/general/header';
import SimilarResults from '../../components/entityDetails/general/similarResults';
import ProvenanceTimeline from '@/components/entityDetails/culturalAsset/provenanceTimeline';
import { PageEntityType } from '@/components/entityDetails/general/types';
import { prep_timeline_data } from '@/components/entityDetails/culturalAsset/provenanceTimeline/bp_podium_example';

export type JointEvent =
  | TransferEvent
  | AcquisitionEvent
  | DepositionEvent
  | ConfiscationEvent
  | RestitutionEvent;

type CulturalAssetPageProps = {
  culturalAsset: CulturalAsset;
  similarCulturalAssets: SimilarEntity_CulturalAsset_[];
  events: JointEvent[];
};

export default function CulturalAssetPage({
  culturalAsset,
  similarCulturalAssets,
  events,
}: CulturalAssetPageProps) {
  const entityType = PageEntityType.CULTURAL_ASSET;
  return (
    <div>
      <Header logoOverflowHidden={true} />
      <Detail entity={{ ...culturalAsset }} entityType={entityType} />
      {similarCulturalAssets.length > 0 && (
        <SimilarResults
          currentEntity={culturalAsset}
          similarEntities={similarCulturalAssets}
          entityType={entityType}
        />
      )}
      {events.length > 0 ? <ProvenanceTimeline events={events} /> : <></>}
    </div>
  );
}

export const getStaticProps: GetStaticProps<CulturalAssetPageProps> = async (
  args,
) => {
  const id = args.params?.id as string;
  const client = apiClient;

  try {
    const asset = await client.culturalAsset.getByIdCulturalAssetGetByIdGet({
      id: id,
    });

    let timeline = asset.events;

    if (id === 'err_73688') timeline = prep_timeline_data;

    return {
      props: {
        culturalAsset: asset.cultural_asset,
        similarCulturalAssets: asset.similar_cultural_assets,
        events: timeline,
      },
    };
  } catch (error) {
    console.log(error);
    return {
      notFound: true,
    };
  }
};

export const getStaticPaths: GetStaticPaths = async () => {
  return {
    // Since there are so many cultural assets, we don't want to pre-render all of them.
    // Fallback: blocking will pre-render them "on the fly" when they are first requested.
    paths: [],
    fallback: 'blocking',
  };
};
