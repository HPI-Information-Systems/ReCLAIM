import { Plus, X } from 'lucide-react';
import { useRouter } from 'next/router';
import { useContext, useEffect, useState } from 'react';

import { FilterContext } from '@/lib/context/FilterContext';
import {
  advancedSearchInputValid,
  useAdvancedSearchQuery,
} from '@/lib/hooks/parser';
import { TooltipModeButton, TooltipSearchButton } from '../general/tooltip';
import { Button } from '../ui/button';
import { SearchFilter } from './filter';
import { TopicDropDown } from './topicDropDown';
import { FormDataEntry } from './searchBox';
import { fetchAutocompleteData } from './autocomplete';

type AdvancedSearchRowProps = {
  index: number;
  topicName: string | null;
  value: string;
  mode: string;
  showRemoveButton: boolean;
  onChangeTopic: (newTopicName: string) => void;
  onChangeValue: (value: string) => void;
  onChangeMode: (mode: 'contains' | 'does not contain') => void;
  onRemove: () => void;
};

function AdvancedSearchRow({
  index,
  topicName,
  value,
  mode,
  showRemoveButton = true,
  onChangeMode,
  onChangeTopic,
  onChangeValue,
  onRemove,
}: AdvancedSearchRowProps) {
  const [autocompleteSuggestions, setAutocompleteSuggestions] = useState<
    string[]
  >([]);

  useEffect(() => {
    const fetchCompletions = async () => {
      try {
        if (topicName)
          setAutocompleteSuggestions(
            await fetchAutocompleteData(value, topicName),
          );
      } catch (e) {
        console.error(e);
      }
    };
    if (value.length > 0) fetchCompletions();
    else setAutocompleteSuggestions([]);
  }, [topicName, value]);

  return (
    <div className="flex item-center justify-center gap-x-3">
      <div className="flex-1 w-48">
        <TopicDropDown currentTopic={topicName} onChangeTopic={onChangeTopic} />
      </div>
      <TooltipModeButton mode={mode} onChangeMode={onChangeMode} />
      <input
        list={'autocomplete-suggestions' + index.toString()}
        className="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
        placeholder="Enter keyword for search here.."
        value={value}
        onChange={(e) => {
          onChangeValue(e.target.value);
        }}
      />
      <datalist id={'autocomplete-suggestions' + index.toString()}>
        {autocompleteSuggestions.map((suggestion, index) => (
          <option key={index} value={suggestion} />
        ))}
      </datalist>
      <Button
        type="button"
        disabled={!showRemoveButton}
        className="disabled:opacity-0 px-1"
        aria-disabled={!showRemoveButton}
        variant={'ghost'}
        onClick={onRemove}
      >
        <X className="text-highlight-blue" />
      </Button>
    </div>
  );
}

export function AdvancedSearch({
  input,
  onChangeInput,
}: {
  input: FormDataEntry[];
  onChangeInput: (input: FormDataEntry[]) => void;
}) {
  const router = useRouter();
  const filterContext = useContext(FilterContext);

  function handleFormSubmit() {
    router.push(useAdvancedSearchQuery(input, filterContext.filter));
  }

  function changeMode(
    input: FormDataEntry[],
    index: number,
    mode: 'contains' | 'does not contain',
  ) {
    const newFormData = [...input];
    newFormData[index].mode = mode;
    onChangeInput(newFormData);
  }

  function changeTopic(
    input: FormDataEntry[],
    index: number,
    newTopicName: string,
  ) {
    const newFormData = [...input];
    newFormData[index].topicName = newTopicName;
    onChangeInput(newFormData);
  }

  function changeValue(input: FormDataEntry[], index: number, value: string) {
    const newFormData = [...input];
    newFormData[index].value = value;
    onChangeInput(newFormData);
  }

  function removeRow(input: FormDataEntry[], index: number) {
    const newFormData = input.filter((_, i) => i !== index);
    onChangeInput(newFormData);
  }

  return (
    <form
      className="p-[2rem] flex flex-col gap-y-3"
      onSubmit={(e) => {
        e.preventDefault();
        handleFormSubmit();
      }}
    >
      {input.map((formRow, index) => (
        <AdvancedSearchRow
          key={index}
          index={index}
          topicName={formRow.topicName}
          value={formRow.value}
          mode={formRow.mode}
          onChangeMode={(mode) => changeMode(input, index, mode)}
          onChangeTopic={(newTopicName) =>
            changeTopic(input, index, newTopicName)
          }
          onChangeValue={(value) => changeValue(input, index, value)}
          showRemoveButton={input.length > 1}
          onRemove={() => removeRow(input, index)}
        />
      ))}
      <div className="inline-flex justify-between items-center h-full">
        <SearchFilter />
        <div className="ml-auto inline-flex gap-x-3">
          <Button
            type="button"
            onClick={() =>
              onChangeInput([
                ...input,
                { topicName: null, value: '', mode: 'contains' },
              ])
            }
            className="bg-highlight-blue"
          >
            <Plus color="white" />
          </Button>

          <TooltipSearchButton
            data="Please fill out all keywords."
            tooltipDisabled={advancedSearchInputValid(input)}
            buttonDisabled={!advancedSearchInputValid(input)}
          />
        </div>
      </div>
    </form>
  );
}
