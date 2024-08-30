import React from 'react';
import { ZoomIn, ZoomOut, Fullscreen } from 'lucide-react';
import { Button, buttonVariants } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import {
  TransformWrapper,
  TransformComponent,
  useControls,
} from 'react-zoom-pan-pinch'; // This package allows us to zoom in and out of images via buttons, by scrolling the mouse wheel, by double clicking on the image or by pinching on touch screens.

export function ImageToolRow({
  imgURL,
  totalNumberOfImages,
  index,
  currentImage,
  inDialog,
}: {
  imgURL: string;
  totalNumberOfImages: number;
  index: number;
  currentImage: number;
  inDialog: boolean;
}) {
  const alttext = 'no-img';
  const Controls = () => {
    const { zoomIn, zoomOut, resetTransform } = useControls();
    const buttonStyle = {
      padding: '10px',
      marginRight: '10px',
      marginTop: '10px',
      marginBottom: '3px',
    };

    return (
      <div
        style={{
          display: 'flex',
          justifyContent: 'flex-end',
          alignItems: 'center',
        }}
      >
        {inDialog && (
          <>
            <Button
              type="button"
              onClick={() => zoomIn()}
              className={cn(
                buttonVariants({ variant: 'outline', shape: 'round' }),
              )}
              style={buttonStyle}
            >
              <ZoomIn color="black" />
            </Button>
            <Button
              type="button"
              onClick={() => zoomOut()}
              className={cn(
                buttonVariants({ variant: 'outline', shape: 'round' }),
              )}
              style={buttonStyle}
            >
              <ZoomOut color="black" />
            </Button>
            <Button
              type="button"
              onClick={() => resetTransform()}
              className={cn(
                buttonVariants({ variant: 'outline', shape: 'round' }),
              )}
              style={buttonStyle}
            >
              <Fullscreen color="black" />
            </Button>
          </>
        )}
        <div className="font-sans text-right text-highlight-blue text-opacity-60 pt-2">
          Image {((index + currentImage) % totalNumberOfImages) + 1}/
          {totalNumberOfImages}
        </div>
      </div>
    );
  };
  return (
    <TransformWrapper>
      <TransformComponent>
        <img
          src={imgURL}
          alt={alttext}
          sizes="100vw"
          style={{ width: 'auto', height: 'auto', margin: 'auto' }}
        />
      </TransformComponent>
      <Controls />
    </TransformWrapper>
  );
}
