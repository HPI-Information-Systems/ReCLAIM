'use client';

import { Button } from '@/components/ui/button';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
} from '@/components/ui/command';
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover';
import { ScrollArea } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { Check, ChevronsUpDown } from 'lucide-react';
import * as React from 'react';
import { TooltipTopic } from '../general/tooltip';
import { TopicContext } from '@/lib/context/TopicContext';

function getTopicCommandItem(
  topicName: string,
  topicTooltip: string,
  isChecked: boolean,
  onSelectTopic: (value: string) => void,
) {
  return (
    <CommandItem key={topicName} value={topicName} onSelect={onSelectTopic}>
      <Check
        className={cn('mr-2 h-4 w-4', isChecked ? 'opacity-100' : 'opacity-0')}
      />
      <TooltipTopic label={topicName} data={topicTooltip} />
    </CommandItem>
  );
}

function listAllTopicOptions({
  currentTopic,
  onChangeTopic,
  setOpen,
}: {
  currentTopic: string | null;
  onChangeTopic: (newTopicName: string) => void;
  setOpen: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const { topics } = React.useContext(TopicContext);

  return (
    <CommandGroup>
      {Array.from(topics).map(([topicName, topicTooltip]) =>
        getTopicCommandItem(
          topicName,
          topicTooltip,
          currentTopic == topicName,
          () => {
            onChangeTopic(topicName);
            setOpen(false);
          },
        ),
      )}
    </CommandGroup>
  );
}

export function TopicDropDown({
  currentTopic,
  onChangeTopic,
}: {
  currentTopic: string | null;
  onChangeTopic: (newTopicName: string) => void;
}) {
  const [open, setOpen] = React.useState(false);

  return (
    <Popover open={open} onOpenChange={setOpen}>
      {/*Box, where the selected topic is displayed in*/}
      <PopoverTrigger asChild className="w-full">
        <Button
          variant="secondary"
          role="combobox"
          aria-expanded={open}
          className="flex min-w-48 w-full justify-between"
          type="button"
        >
          <div className="truncate">{currentTopic || 'Select attribute'}</div>
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>

      {/*Popover Box, where all topic options are displayed in*/}
      <PopoverContent className="w-[300px] p-0 ">
        <ScrollArea className="w-[290px] mt-10 h-[400px]">
          <Command>
            <span className="fixed top-0 w-full">
              <CommandInput placeholder="Search attribute" />
              <CommandEmpty>No attribute found.</CommandEmpty>
            </span>
            {listAllTopicOptions({
              currentTopic,
              onChangeTopic,
              setOpen,
            })}
          </Command>
        </ScrollArea>
      </PopoverContent>
    </Popover>
  );
}
