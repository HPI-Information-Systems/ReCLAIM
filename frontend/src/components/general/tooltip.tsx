import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';
import { Search } from 'lucide-react';
import Link from 'next/link';
import { Button } from '../ui/button';

export function TooltipRow({
  label,
  data,
  rawData,
  link,
}: {
  label: string;
  data: string;
  rawData?: Record<string, string> | (Record<string, string> | null)[] | null;
  link?: string;
}) {
  if (data === '') return null;
  return (
    <>
      <span className="font-bold mb-5 mr-2">{label}</span>
      <span className="mb-5">
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild className="text-left">
              {link ? (
                <Link
                  href={link}
                  className="text-link-color underline visited:text-link-color-visited"
                >
                  {data}
                </Link>
              ) : (
                <span>{data}</span>
              )}
            </TooltipTrigger>
            {rawData && (
              <TooltipContent>
                <div className="flex flex-col items-start text-highlight-blue">
                  <span className="font-bold">Original Records</span>
                  {Array.isArray(rawData)
                    ? rawData.map((rawValue) => {
                        if (rawValue !== null) {
                          return Object.entries(rawValue).map(
                            ([key, value]) => (
                              <span key={key}>
                                {key.replaceAll('_', ' ')}: {value}
                              </span>
                            ),
                          );
                        } else return <></>;
                      })
                    : Object.entries(rawData).map(([key, value]) => (
                        <span key={key}>
                          {key.replaceAll('_', ' ')}: {value}
                        </span>
                      ))}
                </div>
              </TooltipContent>
            )}
          </Tooltip>
        </TooltipProvider>
      </span>
    </>
  );
}

export function TooltipModeButton({
  mode,
  onChangeMode,
}: {
  mode: string;
  onChangeMode: (mode: 'contains' | 'does not contain') => void;
}) {
  return (
    <>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild>
            <Button
              className="bg-highlight-blue min-w-36"
              type="button"
              onClick={(e) => {
                e.preventDefault();
                onChangeMode(
                  mode === 'contains' ? 'does not contain' : 'contains',
                );
              }}
            >
              {mode}
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p>
              {' '}
              Click to switch between <strong>contains</strong> and{' '}
              <strong>does not contain</strong>.{' '}
            </p>
            <p> All rows will be ORed, their order does not matter.</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </>
  );
}

export function TooltipSearchButton({
  data,
  tooltipDisabled,
  buttonDisabled,
}: {
  data: string;
  tooltipDisabled: boolean;
  buttonDisabled: boolean;
}) {
  return (
    <>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger asChild disabled={tooltipDisabled}>
            <Button
              type="submit"
              className={cn(
                ' text-highlight-blue',
                buttonDisabled
                  ? 'bg-background-gray hover:bg-background-gray cursor-not-allowed'
                  : 'bg-highlight-blue',
              )}
              disabled={buttonDisabled}
            >
              <Search color="white" />
            </Button>
          </TooltipTrigger>
          <TooltipContent>
            <p> {data} </p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </>
  );
}

export function ExportButton({ csvLink }: { csvLink: JSX.Element }) {
  return (
    <>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger>{csvLink}</TooltipTrigger>
          <TooltipContent>export data as CSV</TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </>
  );
}

export function TooltipTopic({
  label,
  data,
}: {
  label: string;
  data?: string;
}) {
  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger className="text-left">{label}</TooltipTrigger>
        {data && (
          <TooltipContent className="text-highlight-blue">
            <p>{data}</p>
          </TooltipContent>
        )}
      </Tooltip>
    </TooltipProvider>
  );
}
