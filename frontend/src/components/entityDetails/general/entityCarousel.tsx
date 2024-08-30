import ResultPreview from '@/components/search/searchResults/resultPreview';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel';
import { Collection, CulturalAsset } from '@/lib/client';
import { PageEntityType } from './types';

export function EntityCarousel({
  entites = [],
  entityType,
  headline,
}: {
  entites: CulturalAsset[] | Collection[]; // Add more types as needed
  entityType: PageEntityType;
  headline: string;
}) {
  const assetsPerPage = 4;
  const totalPages = Math.ceil(entites.length / assetsPerPage);

  if (entites.length == 0) return null;

  return (
    <>
      <div className="w-full flex flex-row items-center justify-center mb-5">
        <h1 className="text-3xl grow text-highlight-blue">{headline}</h1>
      </div>

      <Carousel className="w-full mb-10">
        <CarouselContent>
          {Array.from({ length: totalPages }).map((_, index) => (
            <CarouselItem key={index} className="flex flex-col lg:flex-row">
              {entites
                .slice(index * assetsPerPage, (index + 1) * assetsPerPage)
                .map((entity) => (
                  <div
                    key={entity.id}
                    className="min-w-[250px] w-full lg:w-1/4 lg:mx-2 my-2"
                  >
                    <ResultPreview
                      entity={entity}
                      entityType={entityType}
                      isEntityChecked={false}
                      showCheckbox={false}
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
    </>
  );
}
