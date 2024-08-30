import { AVAILABLE_SOURCES } from '@/lib/config/sources';
import { FilterContext } from '@/lib/context/FilterContext';
import { cn } from '@/lib/utils';
import { ChevronsUpDown, FilterIcon } from 'lucide-react';
import { useContext } from 'react';
import { Button } from '../ui/button';
import { Card, CardContent } from '../ui/card';
import { Checkbox } from '../ui/checkbox';
import { Popover, PopoverContent, PopoverTrigger } from '../ui/popover';
import { Switch } from '../ui/switch';

export function SourceFilter() {
  const filterContext = useContext(FilterContext);

  const handleSelectionChange = (name: string) => {
    if (filterContext.filter?.sources.includes(name)) {
      filterContext.removeFilteredSource(name);
    } else {
      filterContext.addFilteredSource(name);
    }
  };

  return (
    <Popover>
      <PopoverTrigger>
        <Button variant="secondary" size={'sm'} type="button" asChild>
          <div className="w-full">
            Sources
            <ChevronsUpDown className="ml-2 h-4 w-4 opacity-50" />
          </div>
        </Button>
      </PopoverTrigger>
      <PopoverContent>
        <div className="flex flex-col gap-y-1">
          {AVAILABLE_SOURCES.map((source, idx) => {
            return (
              <Card
                key={idx}
                className={cn(
                  'flex items-center space-x-2 mb-2 h-full flex-1 hover:cursor-pointer inset-0 border',
                  filterContext.filter?.sources.includes(source.name)
                    ? 'border-primary bg-gray-50'
                    : '',
                )}
                onClick={() => handleSelectionChange(source.name)}
              >
                <CardContent className="flex flex-row items-center h-full py-3 w-full px-1 flex-1 gap-x-3  hover:cursor-pointer">
                  <Checkbox
                    id={`checkbox-${idx}`}
                    isChecked={
                      filterContext.filter?.sources.includes(source.name) ||
                      false
                    }
                    checkHandler={() => handleSelectionChange(source.name)}
                  />
                  <label
                    htmlFor={`checkbox-${idx}`}
                    className="text-sm font-medium peer-disabled:cursor-not-allowed peer-disabled:opacity-70  hover:cursor-pointer select-none leading-4"
                  >
                    <div>{source.label}</div>
                  </label>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </PopoverContent>
    </Popover>
  );
}

export function ImageFilter() {
  const filterContext = useContext(FilterContext);

  return (
    <>
      <div className="flex items-center space-x-2 text-xs">
        <label htmlFor="only-assets-with-images">Require images</label>
        <Switch
          id="only-assets-with-images"
          checked={filterContext.filter?.onlyImages || false}
          onCheckedChange={filterContext.toggleOnlyImages}
        />
      </div>
    </>
  );
}

export function SearchFilter() {
  return (
    <div className="flex items-center gap-x-4 text-sm mt-3">
      <h2 className="text-semibold flex items-center justify-center gap-x-1">
        <FilterIcon
          className="h-5 w-auto text-highlight-blue"
          strokeWidth={0}
          fill="currentColor"
        />
        Filters
      </h2>
      <SourceFilter />
      <ImageFilter />
    </div>
  );
}
