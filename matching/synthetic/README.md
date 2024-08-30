This folder contains the code for the thesis "Synthetic Data for Large Language Model-Based Entity Matching in Provenance Research". The main script for generating the synthetic datasets is `generate_synthetic_data.py`. It is configured to generate the datasets which were used in the course of the experiments that were conducted within the thesis. Datasets are written to the folder `synthetic_output`. New configurations for Ditto are appended to the file `configs.json`, which must be copied (or overwritten) to Ditto's `configs.json` file.

The `columns` folder contains attribute-specific functions which retrieve augmented values for each column (Title and Creator).

The file `augment_synonyms_and_antonyms.docm` was used to retrieve the lists of synonyms and antonyms.

In the `ditto` folder, the gold standard testset is contained.