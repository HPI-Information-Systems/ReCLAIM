## Notice for the munich scraper: Executing this scraper might fail for a larger amount of elements to scrape at a time.
The scraper does not fail for each individual line, but rather for a larger amount of elements to scrape at a time. Because of this, Munich had to be scraped in parts, until this issue is resolved. Running the scraper for all elements results in this error:

```
Loading all elements for munich id 13472 with 5 results.
Loading all elements for munich id 13473 with 4 results.
Loading all elements for munich id 13474 with 6 results.
Loading all elements for munich id 13475 with 5 results.
Loading all elements for munich id 13476 with 4 results.
Loading all elements for munich id 13477 with 3 results.
Loading all elements for munich id 13478 with 6 results.
Loading all elements for munich id 13479 with 3 results.
Loading all elements for munich id 13480 with 5 results.
Loading all elements for munich id 13481 with 4 results.
Loading all elements for munich id 13482 with 4 results.
Loading all elements for munich id 13483 with 3 results.
Loading all elements for munich id 13484 with 6 results.
Traceback (most recent call last):
  File "/home/Antonio.Kruehler/kunstgraph/scraper/scraper.py", line 68, in <module>
    main()
  File "/home/Antonio.Kruehler/kunstgraph/scraper/scraper.py", line 63, in main
    munich_crawler.crawl()
  File "/home/Antonio.Kruehler/kunstgraph/scraper/munich_goering/munich.py", line 140, in crawl
    elements = self.load_all_elements_for_munich_id(str(self.current))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/Antonio.Kruehler/kunstgraph/scraper/munich_goering/munich.py", line 106, in load_all_elements_for_munich_id
    number_of_results = self.get_number_of_results(soup)
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/Antonio.Kruehler/kunstgraph/scraper/munich_goering/munich.py", line 59, in get_number_of_results
    div = html_as_soup.find("div", {"class": "resultheader"})
          ^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'find'
```