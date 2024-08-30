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

export default function AboutPage() {
  return (
    <div>
      <Header logoOverflowHidden={true} />

      <div className="container mx-auto max-w-prose p-8 text-highlight-blue">
        <h1 className="text-4xl font-bold">About the Database</h1>
        <p className="text-lg mt-4">
          Learn more about the Archival Data Repository and its development.
        </p>
      </div>

      <div className="container mx-auto max-w-prose p-8 space-y-8 text-highlight-blue">
        <section>
          <h1 className="text-2xl font-bold mb-3">
            About the Archival Data Repository
          </h1>

          <p className="mb-3 font-sans">
            During the second world war, the National Socialists (Nazis)
            violently and relentlessly persecuted people of Jewish descent in
            Germany and the conquered territories. Part of this persecution was
            the systematic theft of cultural assets. Vast quantities of
            artworks, archives, and libraries were looted, with the objective of
            self-enrichment for the persecutors and annihilation of the culture
            of the persecuted.
          </p>

          <p className="mb-3 font-sans">
            The cultural assets concerned have been handled and documented by
            various actors throughout history, resulting in a large number of
            historical artifacts, both by the perpetrators themselves and by
            allied forces interested in investigation and restitution. Many of
            these artifacts have already been digitized, but are mostly
            available in unstructured form. This representation reduces the
            discoverability of crucial pieces of information for provenance
            researchers and other interested persons.
          </p>

          <p className="mb-3 font-sans">
            In an effort to unify and improve access to these sources, this
            archival data repository integrates various relevant data sources,
            which have been
          </p>

          <ol className="font-sans list-disc ml-4 mb-3">
            <li>
              made machine-processable using OCR technologies & subsequent
              manual reviews,
            </li>
            <li>
              further transformed and processed, improving data quality and
              structure,
            </li>
            <li>
              integrated into a centralized knowledge graph based on the Neo4J
              graph database, and
            </li>
            <li>
              made accessible via the web-based interface you are currently
              visiting.
            </li>
          </ol>

          <p className="mb-3 font-sans">
            Ensuring that any derived data are always backed by the original
            sources at hand is of utmost importance in provenance research. By
            this requirement, the system keeps track of any automated
            improvements during integration, retaining the original source
            information andenabling at-a-glance reviews of the applied
            transformations.
          </p>
        </section>
        <section>
          <h1 className="text-2xl font-bold mb-3">Integrated Data Sources</h1>

          <p className="mb-3 font-sans">
            As of June 2024, the platform integrates data of more than 100.000
            cultural assets from five different archival sources:
          </p>

          <ol className="font-sans list-disc ml-4 mb-3">
            <li>
              <b>Munich Central Collection Point (MCCP)</b> <br />
              integrated using a web scraper for the{' '}
              <a
                href="https://www.dhm.de/datenbank/ccp/dhm_ccp.php?lang=en"
                className="underline"
              >
                DHM MCCP database
              </a>{' '}
              .
            </li>
            <li>
              <b>Marburg Central Collection Point (MaCCP)</b> <br />
              OCR of the property cards and manual review by JDCRP.
            </li>
            <li>
              <b>Wiesbaden Central Collection Point (WCCP)</b> <br />
              OCR of the property cards and manual review by JDCRP.
            </li>
            <li>
              <b>Einsatzstab Reichsleiter Rosenberg (ERR)</b> <br />
              integrated from the relational database powering{' '}
              <a
                href="https://errproject.org/jeudepaume/"
                className="underline"
              >
                errproject.org/jeudepaume/
              </a>
              .
            </li>
            <li>
              <b>Special Commission Linz (SCL)</b> <br />
              integrated using a web scraper for the{' '}
              <a
                href="https://www.dhm.de/datenbank/linzdb/index.html"
                className="underline"
              >
                DHM &quot;Sammlung des Sonderauftrages Linz&quot;
              </a>{' '}
              database.
            </li>
          </ol>
        </section>
        <section>
          <h1 className="text-2xl font-bold mb-3">
            Development of the platform
          </h1>

          <p className="mb-3 font-sans">
            The Jewish Digital Cultural Recovery Project Foundation (JDCRP) was
            founded in 2019 with the goal to build a platform that standardizes
            and links the data of various sources to improve its searchability.
          </p>

          <p className="mb-3 font-sans">
            The Hasso Plattner Institute (HPI) in Potsdam, Germany is a leading
            university for IT-Systems-Engineering. In their final year, HPI
            students commit a large portion of their time to their “bachelor’s
            project”, working on real-world challenges as a team, collaborating
            with an external partner.
          </p>

          <p className="font-sans">
            As part of such a project, a team of eight HPI students worked
            jointly with JDCRP to build an initial version of the archival data
            repository.
          </p>
        </section>
      </div>
      <Footer />
    </div>
  );
}
