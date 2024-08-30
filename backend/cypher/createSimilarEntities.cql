MATCH (n:jdcrp__CulturalAsset) WHERE n.uri CONTAINS "/err/" 
MATCH (m:jdcrp__CulturalAsset) WHERE m.uri CONTAINS "/munich/" AND n.jdcrp__munichNumber = m.jdcrp__munichNumber
CREATE (n)-[:jdcrp__similarEntity {jdcrp__confidence: 1}]->(m)

MATCH (n:jdcrp__CulturalAsset) WHERE n.uri CONTAINS "/err/" 
MATCH (m:jdcrp__CulturalAsset) WHERE m.uri CONTAINS "/linz/" AND n.jdcrp__linzNumber = m.jdcrp__linzNumber
CREATE (n)-[:jdcrp__similarEntity {jdcrp__confidence: 1}]->(m)

MATCH (n:jdcrp__CulturalAsset) WHERE n.uri CONTAINS "/munich/" 
MATCH (m:jdcrp__CulturalAsset) WHERE m.uri CONTAINS "/linz/" AND n.jdcrp__linzNumber = m.jdcrp__linzNumber
CREATE (n)-[:jdcrp__similarEntity {jdcrp__confidence: 1}]->(m)

MATCH (n:jdcrp__CulturalAsset) WHERE n.uri CONTAINS "/munich/" 
MATCH (m:jdcrp__CulturalAsset) WHERE m.uri CONTAINS "/linz/" AND n.jdcrp__munichNumber = m.jdcrp__munichNumber
CREATE (n)-[:jdcrp__similarEntity {jdcrp__confidence: 1}]->(m)