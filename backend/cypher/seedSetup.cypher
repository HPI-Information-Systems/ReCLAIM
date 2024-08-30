CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;

CALL n10s.graphconfig.init();

CALL n10s.nsprefixes.add("kunstgraph","http://kunstgraph.hpi.de/");