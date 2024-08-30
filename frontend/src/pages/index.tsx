import { Header } from '@/components/general/header';
import SearchBox from '@/components/search/searchBox';
import { apiClient } from '@/lib/api/client';
import { TopicContext } from '@/lib/context/TopicContext';
import { GetStaticProps } from 'next';
import Link from 'next/link';
import { useContext, useEffect } from 'react';

function Main() {
  return <main className="flex mb-24 w-full py-[16rem]"></main>;
}

export default function LandingPage({
  topics,
}: {
  topics: Record<string, string>;
}) {
  const backgroundImages = [
    'LI001266',
    'LI001289',
    'LI000160',
    'LI001069',
    'LI000949',
    'LI000077',
    'LI000224',
    'LI001172',
    'LI000003',
  ];

  const randomIndex = Math.floor(Math.random() * backgroundImages.length);
  const randomImage = backgroundImages[randomIndex];
  const backgroundImageJPG = `/background_images/${randomImage}.jpg`;

  const { setTopics } = useContext(TopicContext);

  useEffect(() => {
    setTopics(new Map<string, string>(Object.entries(topics)));
  }, []);

  return (
    <div className="bg-highlight-blue h-screen">
      <Header logoOverflowHidden={false} />
      <Link href={`/culturalAsset/linz_${randomImage}`}>
        {' '}
        <div
          className="w-full h-[30rem] relative"
          style={{
            backgroundImage: `url(${backgroundImageJPG})`,
            backgroundSize: 'cover',
            backgroundPosition: 'center center',
          }}
        ></div>
      </Link>
      <div className="max-lg:hidden absolute top-[90px] right-[20px] text-white text-sm bg-highlight-blue bg-opacity-50 p-2 rounded">
        click on the image to learn more about it
      </div>
      <div className="w-[800px] max-md:w-full max-md:mx-5 left-[50%] absolute top-[450px] translate-x-[-50%]">
        <SearchBox searchQuery={[]} />
      </div>
      <Main />
    </div>
  );
}

export const getStaticProps: GetStaticProps = async () => {
  const client = apiClient;
  try {
    const topics = await client.culturalAsset.getTopicsCulturalAssetTopicsGet();
    return {
      props: {
        topics: topics,
      },
    };
  } catch (error) {
    console.log(error);
    return {
      notFound: true,
    };
  }
};
