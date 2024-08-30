import { Footer } from '@/components/general/footer';
import { TopicContext } from '@/lib/context/TopicContext';
import '@/styles/globals.css';
import type { AppProps } from 'next/app';
import { Libre_Baskerville } from 'next/font/google';
import { useState } from 'react';

const libreBaskerville = Libre_Baskerville({
  weight: ['400', '700'],
  subsets: ['latin'],
});

export default function App({ Component, pageProps }: AppProps) {
  const [topics, setTopics] = useState(pageProps.topics ?? {});

  return (
    <TopicContext.Provider value={{ topics, setTopics }}>
      <div className="flex flex-col min-h-screen">
        <main className={libreBaskerville.className + ' flex-1'}>
          <Component {...pageProps} />
        </main>
        <Footer />
      </div>
    </TopicContext.Provider>
  );
}
