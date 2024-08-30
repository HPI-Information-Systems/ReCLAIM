import { createContext } from 'react';

type TopicContext = {
  topics: Map<string, string>;
  setTopics: (topics: Map<string, string>) => void;
};

export const TopicContext = createContext<TopicContext>({
  topics: new Map<string, string>(),
  setTopics: () => {},
});
