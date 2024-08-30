import { apiClient } from '@/lib/api/client';
import { PersonExtension } from '@/lib/client';
import { GetStaticPaths, GetStaticProps } from 'next';

import Detail from '@/components/entityDetails/general/detail';
import { Header } from '@/components/general/header';
import SimilarResults from '@/components/entityDetails/general/similarResults';
import { PageEntityType } from '@/components/entityDetails/general/types';
import RelatedEntities from '@/components/entityDetails/person/relatedEntities';

type PersonPageProps = {
  person: PersonExtension;
};

export default function PersonPage({ person }: PersonPageProps) {
  return (
    <div>
      <Header logoOverflowHidden={true} />
      <Detail
        entity={{ ...person.person }}
        entityType={PageEntityType.PERSON}
      />
      <RelatedEntities
        createdCulturalAssets={person.cultural_assets_created || []}
        ownedCulturalAssets={person.cultural_assets_owned || []}
        ownedCollections={person.collections_owned || []}
      />
      {person.similar_persons.length > 0 && (
        <SimilarResults
          currentEntity={person.person}
          similarEntities={person.similar_persons}
          entityType={PageEntityType.PERSON}
        />
      )}
    </div>
  );
}

export const getStaticProps: GetStaticProps<PersonPageProps> = async (args) => {
  const id = args.params?.id as string;
  const client = apiClient;

  try {
    const person = await client.person.getByIdPersonGetByIdGet({
      id: id,
    });

    return {
      props: {
        person: person,
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
    // Since there are so many persons, we don't want to pre-render all of them.
    // Fallback: blocking will pre-render them "on the fly" when they are first requested.
    paths: [],
    fallback: 'blocking',
  };
};
