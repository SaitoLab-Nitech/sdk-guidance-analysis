# Data and Code Used in Our Study

- Paper: Detection of Inconsistencies between Guidance Pages and Actual Data Collection of Third-party SDKs in Android Apps
- Conference: 11th International Conference on Mobile Software Engineering and Systems 2024 (MOBILESoft 2024), 15 April 2024, Lisbon, Portugal

Some data are redacted with consideration of respect for the SDK providers.

## Guidance Page Collection

Related files are placed in `guidance_page_collection/`.

### Directory Structure

- (Redacted) `guidance_pages_annotated/`: The guidance pages' screenshots and HTML sources we collected and annotated.
- `gpsdki_crawler.py`: Script used to obtain guidance page links from GPSDKI.
- `guidance_page_downloader.py`: Script used to download guidance pages via links saved in guidance_page_urls_*.txt
- `guidance_page_urls_march_4.txt`: Links obtained from GPSDKI on March 4, 2023.
- `guidance_page_urls_july_4.txt`: Links obtained from GPSDKI on July 4, 2023.
- `guidance_page_urls_july_4_manual_collection.txt`: Links manually collected on July 4, 2023.
- `guidance_page_urls_october_4.txt`: Links obtained from GPSDKI on October 4, 2023.

## Guidance Data Extraction

Related files are placed in `guidance_data_extraction/`.

### Directory Structure

#### Text Extraction

- `extracted_texts/`: Texts extracted from ../guidance_page_collection/guidance_pages_annotated/.
- `text_extraction_for_non-tabular_data.ipynb`: Used to extract texts from non-tabular data in the guidance pages.
- `text_extration_for_table_data.ipynb`: Used to extract texts from tables in the guidance pages.

#### Dataset

- `dataset/`: Used to train and evaluate the machine learning model.
- `dataset_generator.ipynb`: Used to generate the dataset from extracted_texts/.
- `labels.csv`: Named entity types.

#### Evaluation - Scenario 1

Related files are located at `eval_scenario_1/`.

- `fine_tuner.py`: Used to fine-tune a model.
- `evaluator.py`: Used to evaluate the model.
- `evaluator.ipynb`: Used to evaluate the model.

#### Evaluation - Scenario 2

Related files are placed in `eval_scenario_2/`.

- `fine_tuner_1.py`: Used to fine-tune a model for Figure 5.
- `fine_tuner_1.ipynb`: Used to fine-tune a model for Figure 5.
- `evaluator_1.py`: Used to evaluate the model for Figure 5.
- `fine_tuner_2.py`: Used to fine-tune a model for Figure 6.
- `fine_tuner_2.ipynb`: Used to fine-tune a model for Figure 6.
- `evaluator_2.py`: Used to evaluate the model for Figure 6.
- `fine_tuner_3.py`: Used to fine-tune a model for Figure 7.
- `fine_tuner_3.ipynb`: Used to fine-tune a model for Figure 7.
- `evaluator_3.py`: Used to evaluate the model for Figure 7.
- `evaluator.py`: Module used by the other evaluator scripts.


#### Evaluation - Dummy Inconsistency Detection

Related files are located at `eval_dummy_inconsistency_detection/`.

- `helper.py`: Used by inconsistency_detector.py.
- `inconsistency_detector.py`: Main script.
- `map_data_types_to_taint_sources.py`: Data mapping used by inconsistency_detector.py.
- `map_sdks_to_guidance_ids.py`: Used by inconsistency_detector.py.
- `sentiment_analyzer.py`: Sentiment analysis module used by inconsistency_detector.py.
- `answers.py`: Correct answers for this evaluation.
- `extracted_data_for_scenario_1/`: Data extracted by a model for scenario 1.
- `extracted_data_for_scenario_2/`: Data extracted by a model for scenario 2.
- `results_scenario_1/`: Results of scenario 1.
- `results_scenario_2/`: Results of scenario 2.

#### Generating Final Data for Guidance Data Repository

- `inference_runner.ipynb`: Used to run the inference phase.
- `final_outcome_generator.ipynb`: Used to generate final data (e.g., extracted_data_for_inconsistency_detection/) from the inference results.
- `extracted_data_for_inconsistency_detection/`: Extracted data used by ../inconsistency_detection/inconsistency_detector.py.

## SDK Sample App Collection

Related files are located at `sample_app_collection/`.

### Directory Structure

- `collect_and_test_sdks_automatically.py`: Script used to download and build the SDK sample apps.
- `sample_app_repository_urls.txt`: List of GitHub repositories downloaded and built to obtain the SDK sample apps.
- `sdk_configuration.txt`: List of the SDKs configured with google-services.json and API Keys.

## SDK Sample App Analysis

Related files are placed in `sample_app_analysis/`.
Note that the dynamic taint tracker we used (i.e., [T-Recs](https://github.com/SaitoLab-Nitech/T-Recs)) is an open-sourced tool and is not included here.

### Directory Structure

- `results_pixel3_real/`: Analysis results used by ../inconsistency_detection/inconsistency_detector.py.
- `results_pixel6_emul/`: Analysis results used by ../inconsistency_detection/inconsistency_detector.py.
- `results_pixel6_real/`: Analysis results used by ../inconsistency_detection/inconsistency_detector.py.
- `sinks.py`: Taint sinks used by T-Recs.
- `sources.py`: Taint sources used by T-Recs.

## Inconsistency Detection

Related files are located at `inconsistency_detection/`.

### Directory Structure

- (Redacted) `results/`: Inconsistency detection results for 159 APKs.
- `helper.py`: Used by inconsistency_detector.py.
- `inconsistency_detector.py`: Main script.
- `map_data_types_to_taint_sources.py`: Data mapping used by inconsistency_detector.py.
- `map_sdks_to_guidance_ids.py`: Used by inconsistency_detector.py.
- `sentiment_analyzer.py`: Sentiment analysis module used by inconsistency_detector.py.
