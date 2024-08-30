import { SupportedSource } from '@/lib/client';
import { getSourceName } from '@/lib/hooks/getSourceFromSourceAttribute';
import { cn } from '@/lib/utils';

export function SourceContainer({
  source,
  inPreview = false,
}: {
  source: SupportedSource;
  inPreview?: boolean;
}) {
  const commonClasses = 'bg-background-gray rounded-xl font-bold font-sans';
  const previewClasses = 'px-2 py-0.5 text-sm';
  const defaultClasses = 'px-4 py-1 text-lg';

  return (
    <div className={inPreview ? 'mt-2 mb-4' : 'my-8'}>
      <span
        className={cn(
          commonClasses,
          inPreview ? previewClasses : defaultClasses,
        )}
      >
        {inPreview ? getSourceName(source) : `Source: ${getSourceName(source)}`}
      </span>
    </div>
  );
}

export function Title({ data }: { data: string }) {
  return (
    <>
      <span>
        <h1 className="text-highlight-blue text-3xl">{data}</h1>
      </span>
    </>
  );
}
