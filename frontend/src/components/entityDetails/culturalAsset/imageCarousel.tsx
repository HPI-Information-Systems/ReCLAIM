import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { DialogDescription } from '@radix-ui/react-dialog';
import { ImageToolRow } from './imageToolRow';

export default function ImageCarousel({
  imgURLs,
  title,
}: {
  imgURLs: string[];
  title?: string | null;
}) {
  const totalNumberOfImages = imgURLs.length;
  const showArrows = imgURLs.length > 1;

  return (
    <Carousel
      className="w-full px-2 select-none"
      opts={{ loop: true, watchDrag: false }}
    >
      <CarouselContent>
        {imgURLs.map((url, index) => (
          <CarouselItem key={index}>
            <Dialog>
              <DialogTrigger>
                <ImageToolRow
                  imgURL={url}
                  totalNumberOfImages={totalNumberOfImages}
                  index={index}
                  currentImage={0}
                  inDialog={false}
                />
              </DialogTrigger>
              <DialogContent>
                {title ? (
                  <DialogHeader>
                    <DialogTitle>{title}</DialogTitle>
                  </DialogHeader>
                ) : null}
                <DialogDescription>
                  <ImageCarouselInDialog
                    imgURLs={imgURLs}
                    currentImage={index}
                  />
                </DialogDescription>
              </DialogContent>
            </Dialog>
          </CarouselItem>
        ))}
      </CarouselContent>
      {showArrows && <CarouselPrevious />}
      {showArrows && <CarouselNext />}
    </Carousel>
  );
}

function ImageCarouselInDialog(
  /* This function is used when a dialog is opened in the ImageCarousel component.
In the dialog, we also want to display the images in a carousel.
If we would just open ImageCarousel in ImageCarousel, it could get nested infinitely. This problem was not easy to solve with a variable that remembers the depth of the nesting, that's why this function exists. */
  {
    imgURLs,
    currentImage,
  }: {
    imgURLs: string[];
    currentImage: number;
  },
) {
  const totalNumberOfImages = imgURLs.length;
  const showArrows = imgURLs.length > 1;
  imgURLs = imgURLs.slice(currentImage).concat(imgURLs.slice(0, currentImage));

  return (
    <Carousel
      className="w-full px-10 select-none"
      opts={{ loop: true, watchDrag: false }}
    >
      <CarouselContent>
        {imgURLs.map((url, index) => (
          <CarouselItem key={index}>
            <ImageToolRow
              imgURL={url}
              totalNumberOfImages={totalNumberOfImages}
              index={index}
              currentImage={currentImage}
              inDialog={true}
            />
          </CarouselItem>
        ))}
      </CarouselContent>
      {showArrows && <CarouselPrevious className="ml-5" />}
      {showArrows && <CarouselNext className="mr-5" />}
    </Carousel>
  );
}
