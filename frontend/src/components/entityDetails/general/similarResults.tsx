import ResultPreview from '@/components/search/searchResults/resultPreview';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel';
import ComparisonTable from './comparisonTable';
import React from 'react';
import { Button } from '@/components/ui/button';
import {
  CulturalAsset,
  Person,
  SimilarEntity_CulturalAsset_,
  SimilarEntity_Person_,
} from '@/lib/client';
import CSVExport from './csvExport';
import { PageEntityType } from './types';

export default function SimilarResults({
  currentEntity,
  similarEntities = [], // Provide a default value for entities, otherwise it will be undefined and the build process will fail
  entityType,
}: {
  currentEntity: CulturalAsset | Person;
  similarEntities: SimilarEntity_CulturalAsset_[] | SimilarEntity_Person_[];
  entityType: PageEntityType;
}) {
  const entitiesPerPage = 4;
  const totalPages = Math.ceil(similarEntities.length / entitiesPerPage);

  // At first no Checkbox is checked
  const initialEntitiesStatus: { [key: string]: boolean } = {};
  similarEntities.forEach((similarEntity) => {
    initialEntitiesStatus[similarEntity.entity.id] = false;
  });
  // entitiesCheckedStatus contains true at position i if entity i is selected
  const [entitiesCheckedStatus, setEntitiesCheckedStatus] = React.useState(
    initialEntitiesStatus,
  );
  const updateCheckStatus = (id: string) => {
    setEntitiesCheckedStatus({
      ...entitiesCheckedStatus,
      [id]: entitiesCheckedStatus[id] ? false : true,
    });
  };

  // for button to toggle Comparison Mode
  const [comparisonMode, setShowComparisonTable] = React.useState(false);
  const toggleComparisonTable = () => {
    setShowComparisonTable(!comparisonMode);
  };

  // headline is based on entity type
  let headline = `Similar `;
  if (entityType === PageEntityType.CULTURAL_ASSET) {
    headline += 'Cultural Assets';
  } else if (entityType === PageEntityType.PERSON) {
    headline = 'Similar Persons';
  } else if (entityType === PageEntityType.COLLECTION) {
    headline = 'Similar Collections';
  } else {
    throw new Error(
      'This PageEntityType does not have an implementation for similarResults yet',
    );
  }

  return (
    <div className="w-full container pt-10 pb-16 shadow-md rounded-lg my-10 px-10">
      <div className="w-full flex flex-row items-center justify-center mb-10">
        <h1 className="text-3xl grow text-highlight-blue">{headline}</h1>
        <Button
          type="button"
          onClick={() => toggleComparisonTable()}
          className="bg-highlight-blue"
        >
          {comparisonMode
            ? 'Disable Comparison Mode'
            : 'Enable Comparison Mode'}
        </Button>
      </div>

      {/* Carousel shows all similarEntities as Previews with Checkboxes */}
      <Carousel className="w-full">
        <CarouselContent>
          {Array.from({ length: totalPages }).map((_, index) => (
            <CarouselItem key={index} className="flex flex-col lg:flex-row">
              {similarEntities
                .slice(index * entitiesPerPage, (index + 1) * entitiesPerPage)
                .map((similarEntity) => (
                  <div
                    key={similarEntity.entity.id}
                    className="min-w-[250px] w-full lg:w-1/4 lg:mx-2 my-2"
                  >
                    <ResultPreview
                      entity={similarEntity.entity}
                      entityType={entityType}
                      updateCheckStatus={updateCheckStatus}
                      isEntityChecked={
                        entitiesCheckedStatus[similarEntity.entity.id]
                      }
                      showCheckbox={comparisonMode}
                    />
                  </div>
                ))}
            </CarouselItem>
          ))}
        </CarouselContent>
        {totalPages > 1 ? (
          <>
            <CarouselPrevious />
            <CarouselNext />
          </>
        ) : null}
      </Carousel>

      {/* The current entity is always the first column. All similarEntities whose checkboxes are selected are added */}
      {comparisonMode && (
        <div>
          <ComparisonTable
            similarEntities={[
              currentEntity,
              ...similarEntities
                .sort((a, b) => b.confidence - a.confidence)
                .map((similarEntity) => similarEntity.entity)
                .filter(
                  (entity) => entitiesCheckedStatus[entity.id], // order of entities is as in similarEntities, not the order in which they were checked
                ),
            ]}
            entityType={entityType}
          />

          <CSVExport
            currentEntity={currentEntity}
            similarEntities={similarEntities.map(
              (similarEntity) => similarEntity.entity,
            )}
            entitiesCheckedStatus={entitiesCheckedStatus}
            entityType={entityType}
          />
        </div>
      )}
    </div>
  );
}
