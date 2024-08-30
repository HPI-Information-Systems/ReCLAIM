import { EntryType } from '../general/types';

// Keep this updated with CulturalAsset
// Order of the keys is the order in which they are displayed
export const culturalAssetProperties = {
  title: { label: 'Title', type: EntryType.ATTRIBUTE },
  collected_in: { label: 'Collection', type: EntryType.RELATION_WITH_LINK },
  classified_as: { label: 'Classification', type: EntryType.RELATION },
  consists_of_material: { label: 'Material', type: EntryType.RELATION },
  created_by: { label: 'Creator', type: EntryType.RELATION_WITH_LINK },
  creation_date: { label: 'Creation Date', type: EntryType.ATTRIBUTE },
  structured_creation_date: {
    label: 'Structured Creation Date',
    type: EntryType.ATTRIBUTE,
  },
  created_in_location: { label: 'Creation Location', type: EntryType.RELATION },
  located_in: { label: 'Location', type: EntryType.RELATION },

  measurements: { label: 'Measurements', type: EntryType.ATTRIBUTE },
  weight: { label: 'Weight', type: EntryType.ATTRIBUTE },
  annotation: { label: 'Annotation', type: EntryType.ATTRIBUTE },
  identifying_marks: { label: 'Identifying Marks', type: EntryType.ATTRIBUTE },
  archival_source_description: {
    label: 'Archival Source Description',
    type: EntryType.ATTRIBUTE,
  },
  physical_description: {
    label: 'Physical Description',
    type: EntryType.ATTRIBUTE,
  },
  physical_condition_description: {
    label: 'Physical Condition Description',
    type: EntryType.ATTRIBUTE,
  },
  provenance_description: {
    label: 'Provenance Description',
    type: EntryType.ATTRIBUTE,
  },
  pre_confiscation_history_description: {
    label: 'Pre-Confiscation History Description',
    type: EntryType.ATTRIBUTE,
  },
  post_confiscation_history_description: {
    label: 'Post-Confiscation History Description',
    type: EntryType.ATTRIBUTE,
  },
  current_remain_description: {
    label: 'Current Remain Description',
    type: EntryType.ATTRIBUTE,
  },
  wccp_number: { label: 'Wiesbaden Number', type: EntryType.ATTRIBUTE },
  marburg_number: { label: 'Marburg Number', type: EntryType.ATTRIBUTE },
  munich_number: { label: 'Munich Number', type: EntryType.ATTRIBUTE },
  linz_number: { label: 'Linz Number', type: EntryType.ATTRIBUTE },
  err_number: { label: 'ERR Number', type: EntryType.ATTRIBUTE },
  inventory_number: {
    label: 'Inventory Number',
    type: EntryType.ATTRIBUTE,
  },
  catalog_number: {
    label: 'Catalogue Number',
    type: EntryType.ATTRIBUTE,
  },
  negative_number: {
    label: 'Negative Number',
    type: EntryType.ATTRIBUTE,
  },
  claim_number: { label: 'Claim Number', type: EntryType.ATTRIBUTE },
  shelf_number: { label: 'Shelf Number', type: EntryType.ATTRIBUTE },
  information_on_images: {
    label: 'Image Information',
    type: EntryType.ATTRIBUTE,
  },
  copies_of_card: { label: 'Copies of Card', type: EntryType.ATTRIBUTE },
  bibliography: { label: 'Bibliography', type: EntryType.ATTRIBUTE },
  bundesarchiv_band: { label: 'Bundesarchiv Band', type: EntryType.ATTRIBUTE },
  bundesarchiv_signature: {
    label: 'Bundesarchiv Signature',
    type: EntryType.ATTRIBUTE,
  },
  bundesarchiv_title: {
    label: 'Bundesarchiv Title',
    type: EntryType.ATTRIBUTE,
  },
  bundesarchiv_start_date: {
    label: 'Bundesarchiv Start Date',
    type: EntryType.ATTRIBUTE,
  },
  bundesarchiv_end_date: {
    label: 'Bundesarchiv End Date',
    type: EntryType.ATTRIBUTE,
  },
  bundesarchiv_property_card_file_name_front: {
    label: 'Bundesarchiv Property Card Filename Front',
    type: EntryType.ATTRIBUTE,
  },
  bundesarchiv_property_card_file_name_back: {
    label: 'Bundesarchiv Property Card Filename Back',
    type: EntryType.ATTRIBUTE,
  },

  /*depicted_in_image: {label: "Depicted In Image", type: EntryType.RELATION},
    referenced_in_card_image: {label: "Referenced In Card Image", type: EntryType.RELATION},*/
} as const;
