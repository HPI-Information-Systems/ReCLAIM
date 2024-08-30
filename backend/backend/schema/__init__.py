##################################################
### Notice: This schema file is auto-generated from the ontology using the generate_backend_schema.py.
### Do not make changes to this file directly. Instead, modify the ontology and then re-generate this file.
##################################################


from typing import List, Optional
from .base_schema import *


class Collection(EntityModel):
    abbreviation: Optional[Entry[str]] = None
    owned_by: Optional["Person"] = None
    name: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class CulturalAsset(EntityModel):
    annotation: Optional[Entry[str]] = None
    bibliography: Optional[Entry[str]] = None
    bundesarchiv_band: Optional[Entry[str]] = None
    bundesarchiv_end_date: Optional[Entry[str]] = None
    bundesarchiv_property_card_file_name_back: Optional[Entry[str]] = None
    bundesarchiv_property_card_file_name_front: Optional[Entry[str]] = None
    bundesarchiv_signature: Optional[Entry[str]] = None
    bundesarchiv_start_date: Optional[Entry[str]] = None
    bundesarchiv_title: Optional[Entry[str]] = None
    catalog_number: Optional[Entry[str]] = None
    claim_number: Optional[Entry[str]] = None
    classified_as: Optional[List["Classification"]] = None
    consists_of_material: Optional[List["Material"]] = None
    copies_of_card: Optional[Entry[str]] = None
    created_by: Optional["Person"] = None
    created_in_location: Optional["Location"] = None
    creation_date: Optional[Entry[str]] = None
    current_remain_description: Optional[Entry[str]] = None
    depicted_in_image: Optional[List["Image"]] = None
    err_number: Optional[Entry[str]] = None
    identifying_marks: Optional[Entry[str]] = None
    information_on_images: Optional[Entry[str]] = None
    inventory_number: Optional[Entry[str]] = None
    linz_number: Optional[Entry[str]] = None
    located_in: Optional["Location"] = None
    marburg_number: Optional[Entry[str]] = None
    measurements: Optional[Entry[str]] = None
    munich_number: Optional[Entry[str]] = None
    negative_number: Optional[Entry[str]] = None
    physical_condition_description: Optional[Entry[str]] = None
    post_confiscation_history_description: Optional[Entry[str]] = None
    pre_confiscation_history_description: Optional[Entry[str]] = None
    provenance_description: Optional[Entry[str]] = None
    referenced_in_card_image: Optional[List["Image"]] = None
    referenced_in_card_image_back: Optional[List["Image"]] = None
    referenced_in_card_image_front: Optional[List["Image"]] = None
    shelf_number: Optional[Entry[str]] = None
    structured_creation_date: Optional[Entry[str]] = None
    title: Optional[Entry[str]] = None
    wccp_number: Optional[Entry[str]] = None
    weight: Optional[Entry[str]] = None
    collected_in: Optional["Collection"] = None
    archival_source_description: Optional[Entry[str]] = None
    physical_description: Optional[Entry[str]] = None


class TransferEvent(EntityModel):
    arrival_date: Optional[Entry[str]] = None
    departure_date: Optional[Entry[str]] = None
    from_location: Optional["Location"] = None
    identified_by: Optional[List["Institution | LegalEntity | Person"]] = None
    physical_description_after: Optional[Entry[str]] = None
    physical_description_before: Optional[Entry[str]] = None
    possessor_after: Optional[List["Institution | LegalEntity | Person"]] = None
    possessor_before: Optional[List["Institution | LegalEntity | Person"]] = None
    structured_arrival_date: Optional[Entry[str]] = None
    structured_departure_date: Optional[Entry[str]] = None
    to_collection: Optional["Collection"] = None
    to_location: Optional["Location"] = None
    by_legal_entity: Optional["Institution | LegalEntity | Person"] = None
    from_collection: Optional[List["Collection"]] = None
    affected_cultural_asset: Optional["CulturalAsset"] = None
    relative_order: int
    with_involvement_of: Optional[List["Person"]] = None
    physical_description: Optional[Entry[str]] = None
    date: Optional[Entry[str]] = None
    structured_date: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class Person(EntityModel):
    birth_date: Optional[Entry[str]] = None
    born_in_location: Optional["Location"] = None
    death_date: Optional[Entry[str]] = None
    died_in_location: Optional["Location"] = None
    first_name: Optional[Entry[str]] = None
    history_description: Optional[Entry[str]] = None
    last_name: Optional[Entry[str]] = None
    lifetime: Optional[Entry[str]] = None
    pseudonym: Optional[Entry[str]] = None
    structured_birth_date: Optional[Entry[str]] = None
    structured_death_date: Optional[Entry[str]] = None
    based_in: Optional["Location"] = None
    archival_source_description: Optional[Entry[str]] = None
    name: Optional[Entry[str]] = None


class Location(EntityModel):
    city: Optional[Entry[str]] = None
    country: Optional[Entry[str]] = None
    latitude: Optional[Entry[float]] = None
    longitude: Optional[Entry[float]] = None
    part_of: Optional["Location"] = None
    region: Optional[Entry[str]] = None
    street: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class DepositionEvent(EntityModel):
    deposited_by: Optional[List["Institution | LegalEntity | Person"]] = None
    depot_number: Optional[Entry[str]] = None
    possessor: Optional[List["Institution | LegalEntity | Person"]] = None
    collected_in: Optional["Collection"] = None
    at_location: Optional["Location"] = None
    affected_cultural_asset: Optional["CulturalAsset"] = None
    relative_order: int
    with_involvement_of: Optional[List["Person"]] = None
    physical_description: Optional[Entry[str]] = None
    date: Optional[Entry[str]] = None
    structured_date: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class RestitutionEvent(EntityModel):
    restituted_to_legal_entity: Optional["Institution | LegalEntity | Person"] = None
    at_location: Optional["Location"] = None
    affected_cultural_asset: Optional["CulturalAsset"] = None
    relative_order: int
    with_involvement_of: Optional[List["Person"]] = None
    physical_description: Optional[Entry[str]] = None
    date: Optional[Entry[str]] = None
    structured_date: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class Classification(TaxonomyModel):
    sub_classification_of: Optional["Classification"] = None
    wikidata_uri: Optional[Entry[str]] = None
    name: Optional[Entry[str]] = None


class Material(TaxonomyModel):
    sub_material_of: Optional[List["Material"]] = None
    wikidata_uri: Optional[Entry[str]] = None
    name: Optional[Entry[str]] = None


class Image(EntityModel):
    url: str


class AcquisitionEvent(EntityModel):
    acquisition_cost: Optional[Entry[str]] = None
    through_legal_entity: Optional[List["Institution | LegalEntity | Person"]] = None
    from_legal_entity: Optional[List["Institution | LegalEntity | Person"]] = None
    by_legal_entity: Optional["Institution | LegalEntity | Person"] = None
    from_collection: Optional[List["Collection"]] = None
    at_location: Optional["Location"] = None
    affected_cultural_asset: Optional["CulturalAsset"] = None
    relative_order: int
    with_involvement_of: Optional[List["Person"]] = None
    physical_description: Optional[Entry[str]] = None
    date: Optional[Entry[str]] = None
    structured_date: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class LegalEntity(EntityModel):
    based_in: Optional["Location"] = None
    archival_source_description: Optional[Entry[str]] = None
    name: Optional[Entry[str]] = None


class ConfiscationEvent(EntityModel):
    from_legal_entity: Optional[List["Institution | LegalEntity | Person"]] = None
    by_legal_entity: Optional["Institution | LegalEntity | Person"] = None
    from_collection: Optional[List["Collection"]] = None
    at_location: Optional["Location"] = None
    affected_cultural_asset: Optional["CulturalAsset"] = None
    relative_order: int
    with_involvement_of: Optional[List["Person"]] = None
    physical_description: Optional[Entry[str]] = None
    date: Optional[Entry[str]] = None
    structured_date: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class CulturalAssetEvent(EntityModel):
    affected_cultural_asset: Optional["CulturalAsset"] = None
    relative_order: int
    with_involvement_of: Optional[List["Person"]] = None
    physical_description: Optional[Entry[str]] = None
    date: Optional[Entry[str]] = None
    structured_date: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class Event(EntityModel):
    date: Optional[Entry[str]] = None
    structured_date: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class ForcedSaleEvent(EntityModel):
    acquisition_cost: Optional[Entry[str]] = None
    through_legal_entity: Optional[List["Institution | LegalEntity | Person"]] = None
    from_legal_entity: Optional[List["Institution | LegalEntity | Person"]] = None
    by_legal_entity: Optional["Institution | LegalEntity | Person"] = None
    from_collection: Optional[List["Collection"]] = None
    at_location: Optional["Location"] = None
    affected_cultural_asset: Optional["CulturalAsset"] = None
    relative_order: int
    with_involvement_of: Optional[List["Person"]] = None
    physical_description: Optional[Entry[str]] = None
    date: Optional[Entry[str]] = None
    structured_date: Optional[Entry[str]] = None
    description: Optional[Entry[str]] = None


class Institution(EntityModel):
    based_in: Optional["Location"] = None
    archival_source_description: Optional[Entry[str]] = None
    name: Optional[Entry[str]] = None
