import argparse

import munich_goering.goering as goering
import munich_goering.munich as munich

parser = argparse.ArgumentParser(description="Scrape the DHM datasets.")
parser.add_argument(
    "--goering", "-g", help="Scrape the Goering collection", action="store_true"
)
parser.add_argument(
    "--munich",
    "-m",
    help="Scrape the Munich Central Collecting Point collection",
    action="store_true",
)
parser.add_argument(
    "--limit",
    "-l",
    help="The limit of datapoints to scrape for each endpoint",
    default=100,
    type=int,
)
parser.add_argument(
    "--start_munich",
    "-sm",
    help="The starting munich ID to start scraping from",
    default=1,
    type=int,
)
parser.add_argument(
    "--start_goering",
    "-sg",
    help="The starting goering ID to start scraping from",
    default=1,
    type=int,
)
parser.add_argument(
    "--wait",
    "-w",
    help="The time (in ms) to wait between requests",
    default=100,
    type=int,
)

args = parser.parse_args()


def main():
    if args.goering:
        print(
            "Please note that limit, wait and start are not yet implemented for the Goering collection."
        )
        print(
            "The scraper will continue to scrape every element within this collection."
        )
        goering.goering_alpha()

    if args.munich:
        munich_crawler = munich.MunichCrawler(
            limit=int(args.limit), start=int(args.start_munich), wait=int(args.wait)
        )

        munich_crawler.crawl()
        munich_crawler.save()


if __name__ == "__main__":
    main()
