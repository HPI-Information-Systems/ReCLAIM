import { Footer } from '@/components/general/footer';
import { Header } from '@/components/general/header';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

function buildAccordionItem(id: string, question: string, answer: string[]) {
  return (
    <AccordionItem value={id}>
      <AccordionTrigger>{question}</AccordionTrigger>
      <AccordionContent>
        {answer.map((item, index) => (
          <p className="mb-3 font-sans" key={index}>
            {item}
          </p>
        ))}
      </AccordionContent>
    </AccordionItem>
  );
}

export default function HelpPage() {
  return (
    <div>
      <Header logoOverflowHidden={true} />

      <div className="container mx-auto p-8 text-highlight-blue">
        <h1 className="text-4xl font-bold">Help</h1>
        <p className="text-lg mt-4">
          Here you can find information on how to use this platform.
        </p>
      </div>

      <div className="container mx-auto p-8 text-highlight-blue">
        <Accordion type="single" collapsible className="w-full">
          <h1 className="text-2xl font-bold">Search</h1>
          {buildAccordionItem('search', 'How do I search for something?', [
            'To search the data, there is a box on the home page and on the search page where you can enter the keywords you are looking for. If you want to search for specific attributes by keyword, you can click on "Advanced Search" at the top of the box.',
          ])}
          {buildAccordionItem(
            'fulltext_search',
            'How does the "Search" mode work?',
            [
              'If you are in "Search" mode, only one row will appear in the search box in which you can enter terms you are looking for. Then press the button with the magnifying glass to carry out the search. The search results you find must contain all the words in your search query somewhere in their data. ',
            ],
          )}
          {buildAccordionItem(
            'advanced_search',
            'How does the "Advanced Search" mode work?',
            [
              'If you are in Advanced Search mode, you can click "Select Keyword" on the left to select a keyword to search for specific terms. Next to it is a button that says "contains". You can click this to toggle between "contains" and "does not contain". Finally, you can enter your keywords in the text field.',
              'For example, Material: Name does not contain oil means that all the results that follow will not have oil as a material, e.g. not oil paint. ',
              'The query CulturalAsset: Linz Number contains 123 returns all cultural objects whose Linz number contains the substring 123. ',
              'The input field can also be left empty. The query CulturalAsset: Linz number contains and then a free input field returns, for example, all Cultural Assets that have a Linz number. ',
              'The button with the plus symbol can be used to add another row to search for specific keywords on another attribute. The rows are then linked with AND in the query. Once there are at least two rows, you can also delete rows with the X that appears on the right.',
            ],
          )}
          {buildAccordionItem('keywords', 'What do the keywords mean?', [
            'To find out the meaning of keywords in Advanced Search, you can hover over the words in the dropdown. If you leave your cursor still for a moment, an explanation of the respective keyword will appear.',
          ])}
          {buildAccordionItem(
            'autocomplete',
            'What does the autocompletion show me?',
            [
              'The autocompletion shows you the first 10 possible values that a selected keyword can take that match your current input in the row. Note that there may be more than 10 corresponding inputs, as we only show 10 at a time.',
            ],
          )}

          <h1 className="mt-10 text-2xl font-bold">Search Results</h1>
          {buildAccordionItem(
            'search_results_location',
            'Where can I find search results?',
            [
              'You can access the results page by clicking on "Search" at the top of the header or by starting the search from the home page by clicking the button with the magnifying glass.',
            ],
          )}
          {buildAccordionItem(
            'search_results_explanation',
            'What do the search results show me?',
            [
              'As a search result, you get back all cultural assets that match your search query. If your search query is empty, all cultural assets will be displayed. Initially, you will only receive a preview of the results. To get more information about a cultural asset, simply click on the titles in the preview boxes.',
            ],
          )}
          {buildAccordionItem(
            'search_results_all',
            'How can I see all cultural assets there are in the database?',
            [
              'If your search query is empty, all cultural assets will be displayed.',
            ],
          )}

          <h1 className="mt-10 text-2xl font-bold">Detail Page</h1>
          {buildAccordionItem('detail_page', 'What is a detail page?', [
            'A detail page is a page where you can learn more about a cultural asset or a person, for example. If you click on a search result preview box, for example, you will be taken to a detail page for this cultural asset. If you then click on the name of the creator again, you will be taken to a person detail page. ',
            'You can always see where the information on a detail page comes from in the source information under the title.',
          ])}
          {buildAccordionItem(
            'original_values',
            'What are original values and where can I find them?',
            [
              'There are prepared values and original values.',
              ' What you initially see when you look at a detail page are prepared values. These are created from the original values using various carefully created algorithms. ',
              'Original values are the data that was read from scans of property cards using OCR, for example. Errors may have occurred where, for example, a B was read as 8. Sometimes the data from one field has also been split into several fields, e.g. names that have been split into first name and surname. The original values can be seen by hovering over the corresponding entry in a line. Alternatively, the index cards, which in many cases can be seen as an image, also provide information.',
            ],
          )}
          {buildAccordionItem(
            'image_view',
            'How can I increase the size of the images on the detail page?',
            [
              'To increase the size of the images, simply click on the image. It will then increase in size according to the size of your browser window.',
            ],
          )}

          {/* Add more AccordionItems here, when new features are ready */}
        </Accordion>
      </div>
      <Footer />
    </div>
  );
}
