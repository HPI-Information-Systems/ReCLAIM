## How to insert data sources
Create a directory for each data source with its name. Add a README.md with an interpretation of the data.

## Overview of data sources

### Data source classification
<table>
    <tr>
        <td><strong>Name</strong></td>
        <td><strong>Information</strong></td>
        <td><strong>Website</strong></td>
        <td><strong>Contact</strong></td>
        <td><strong>Integration Status</strong></td>
    </tr>
    <tr>
        <td>MCCP</td>
        <td>https://de.wikipedia.org/wiki/Munich_Central_Collecting_Point</td>
        <td>https://www.dhm.de/datenbank/ccp/dhm_ccp.php?lang=en</td>
        <td>-</td>
        <td>data publically available, built scraper</td>
    </tr>
    <tr>
        <td>Linz</td>
        <td>https://de.wikipedia.org/wiki/Sonderauftrag_Linz</td>
        <td>https://www.dhm.de/datenbank/linzdb/linzform2.html</td>
        <td>-</td>
        <td>data publically available, built scraper</td>
    </tr>
    <tr>
        <td>WCCP</td>
        <td>https://de.wikipedia.org/wiki/Wiesbaden_Central_Collecting_Point</td>
        <td>-</td>
        <td>-</td>
        <td>data offcially provided, etl in preparation</td>
    </tr>
    <tr>
        <td>ERR</td>
        <td>https://de.wikipedia.org/wiki/Einsatzstab_Reichsleiter_Rosenberg</td>
        <td>https://www.errproject.org/jeudepaume/</td>
        <td>-</td>
        <td>data officially provided but also publically available on website - public source has more data though, built scraper, etl in preparation</td>
    </tr>
    <tr>
        <td>LostLift</td>
        <td>"Soweit aus den Dokumenten ersichtlich, rekonstruiert jeder Eintrag den Weg des Umzugsgutes einer Eigentümerfamilie - vom Verlassen der Wohnung mit einem Spediteur bis zur Beschlagnahmung in einer Hafenstadt und schließlich der Versteigerung des Eigentums." - see website</td>
        <td>https://lostlift.dsm.museum/</td>
        <td>lostlift@dsm.museum</td>
        <td>in prospect, data is publically available</td>
    </tr>
    <tr>
        <td>lootedart.com</td>
        <td>"The Central Registry of Information on Looted Culturalm Property 1933-1945", consists of information database with documentations from 49 countries and object database with 25,000 objects - see website. Object database is probably most interesting for our use case - "25,000 objects of all kinds – paintings, drawings, antiquities, Judaica, etc – looted, missing and/or identified from over fifteen countries. All images on the site are published under fair use conditions for the purpose of criticism and research." </td>
        <td>https://lootedart.com/home</td>
        <td>info@lootedart.com</td>
        <td>in prospect, data available (publically)</td>
    </tr>
    <tr>
        <td>OFP</td>
        <td>"Provenienzforschung anhand von personenbezogenen Akten: Die rund 42.000 Akten des Bestandes Rep. 36A Oberfinanzpräsident Berlin-Brandenburg (II) dokumentieren die Arbeit der nationalsozialistischen „Vermögensverwertungsstelle“ und damit die systematische Verwertung des Vermögens von als jüdisch oder reichsfeindlich verfolgten Personen" - see website. OFP provided lootedart.com access to their first digitalization results in Oct. 2023</td>
        <td>https://blha.brandenburg.de/index.php/projekte/ofp-projekt/</td>
        <td>poststelle@blha.brandenburg.de</td>
        <td>in prospect, data not yet completely digitalized but first results digital, digital part is partially available in lootedart.com</td>
    </tr>
    <tr>
        <td>KVDB - Kunstverwaltung des Bundes</td>
        <td>"Über die Provenienzdatenbank.Bund können die bisherigen Ergebnisse der systematischen Untersuchung der Gemälde, Grafiken, Skulpturen sowie kunstgewerblichen und archäologischen Objekte abgerufen werden, die vor dem Jahre 1945 entstanden sind und sich heute im Besitz der Bundesrepublik Deutschland befinden. Der überwiegende Teil dieser Werke stammt aus dem ehemaligen Central Collecting Point (CCP) München." - see website, better UI than Linz and MCCP, "über 2000 erfasste Kunstwerke" - could be subset of Linz & MCCP</td>
        <td>https://kunstverwaltung.bund.de/DE/Home/home_node.html, https://kunstverwaltung.bund.de/SiteGlobals/Forms/Suche/Provenienzrecherche/Provenienzrecherche_Formular.html?nn=850008</td>
        <td>https://kunstverwaltung.bund.de/DE/Service/Kontakt/kontakt_node.html</td>
        <td>in prospect, data is publically available</td>
    </tr>
    <tr>
        <td>Moses Meldessohn Stiftung</td>
        <td>"Unter dem Motto »Das deutsch-jüdische Kulturerbe sichern« betreibt die Moses Mendelssohn Stiftung in Kooperation mit dem Moses Mendelssohn Zentrum, dem Fraunhofer Institut (IPK) und weiteren wissenschaftlichen Einrichtungen ein weltweit weitreichendes wissenschaftliches Projekt, welches das Erkennen, Erfassen und Bewahren von kulturellem Erbe des deutschsprachigen Judentums sowohl in ihren Herkunfts- als auch in den Auswanderungsländern zum Ziel hat." - see website, this organization is probably involved in multiple projects regarding cultural assets</td>
        <td>https://www.moses-mendelssohn-stiftung.de/</td>
        <td>General: willkommen(at)moses-mendelssohn-stiftung.de,
        Contact Person: Julius.Schoeps(at)mendelssohnstiftung.com / Elke-Vera.Kotowski(at)mendelssohnstiftung.com</td>
        <td>in prospect, no data publically available</td>
    </tr>
    <tr>
        <td>Provena / Lost Art</td>
        <td>"Proveana ist die Forschungsdatenbank des Deutschen Zentrums Kulturgutverluste. [...] Die Datenbank erlaubt die Suche nach Personen, Körperschaften, Ereignissen, Sammlungen, Provenienzmerkmalen, Objekten und weiterführenden Quellen. Proveana durchsucht auch die Inhalte der Lost Art-Datenbank und stellt Verknüpfungen zu weiteren Datenbanken her." - see website (also: https://kulturgutverluste.de/)</td>
        <td>https://www.proveana.de/de/start</td>
        <td>proveana@kulturgutverluste.de</td>
        <td>in prospect, data publically available</td>
    </tr>
    <tr>
        <td>zdk</td>
        <td>"Die Website ermöglicht erstmals die parallele Recherche in zwei zusammengehörenden Quellen zum nationalsozialistischen Kunstraub, die sich in zwei unterschiedlichen Institutionen in Wien befinden: dem Archiv des Kunsthistorischen Museums und dem Archiv des Bundesdenkmalamts, das von der Kommission für Provenienzforschung betreut wird." - see https://www.zdk-online.org/</td>
        <td>https://www.zdk-online.org/suche/</td>
        <td>kontakt@zdk-online.org</td>
        <td>in prospect, data publically available</td>
    </tr>
    <tr>
        <td>Getty Provenance Index</td>
        <td>"At the heart of its operations is the Getty Provenance Index®, which currently contains more than 2.3 million records taken from source material such as archival inventories, auction catalogs, and dealer stock books.", also there are additional databases referenced (https://www.getty.edu/research/tools/provenance/, https://piprod.getty.edu/starweb/piadd/servlet.starweb?path=piadd/piadd.web)</td>
        <td>https://piprod.getty.edu/starweb/pi/servlet.starweb?path=pi/pi.web https://github.com/thegetty/provenance-index-csv/tree/main</td>
        <td>Questions regarding reference: reference@getty.edu, General Contact: https://fmweb.getty.edu/griscrr/reference_form.php</td>
        <td>in prospect, largest database so far, data publically available and under CCO 1.0 freely usable.</td>
    </tr>
</table>

### Other links to be classified and analyzed
- https://www.culture.gouv.fr/Nous-connaitre/Organisation-du-ministere/Le-secretariat-general/Mission-de-recherche-et-de-restitution-des-biens-culturels-spolies-entre-1933-et-1945/Recherche-de-provenance-outils-et-methode/Repertoire-des-biens-spolies-RBS#acces
- https://lootedart.belgium.be/en
- https://www.fold3.com/
- https://www.civs.gouv.fr/en/spoliated-cultural-property/ted-database/
- https://www.geschkult.fu-berlin.de/e/db_entart_kunst/index.html
- https://www.artnet.de/
- https://de.artprice.com/
- https://heinemann.gnm.de/de/willkommen.html
- http://boehler.zikg.eu/solr-suche
- https://www.uni-marburg.de/de/fotomarburg
- https://www.lootedculturalassets.de/
- provenienzforschung.commsy.net
- wga-datenbank.de
- search.arch.be
