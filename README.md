# ML4ClimateAdaptationPolicy

It is important that you do not change the names of any folders
or files before finishing the pipeline. 
Doing so, may raise errors as the scripts look in folders
with these specific names.

Step 1:
In the folder 'PDF_files' the PDF documents are contained.
'Adaptation policy documents' - Training data for adaptation policies
'Mitigation policy documents' - Training data for mitigation policies
'Non-climate policy documents' - Training data for non-climate documents
'Mixed policy documents' - Testing data, any PDF document(s) you want to predict on.

Step 2:
In the folder 'Python Scripts' every script in the pipeline is contained.
MAIN PIPELINE
'pdf_parser.py' - Extract raw text from PDf documents (parsed_files)
'text_cleanup.py' - Filters, cleansand structurizes data into 'bags-of-words' (structured_files)
'sqlite_db.py' - Builds database and inserts cleaned data (climate.db)
'numberizer.py' - Builds vocabulary from training data (conversion_dictionary.txt)
'TF_classification_BW.py' - Builds neural network and stores it (tensorflow/logdir)
'TF_classification_predict.py' - Uses stored model to predict on new data. Results stored in database.
OPTIONAL
'pipeline.py' - Runs every script in the main pipeline in order. MAY FAIL AT THE FIRST STEP
'web_scraper.py' - Retrieves documents from https://www.gov.uk/government/publications?keywords=&taxons[]=all&subtaxons[]=all&publication_filter_option=policy-papers&departments[]=all&official_document_status=all&world_locations[]=all&from_date=&to_date= (PDF_files\Scraped documents)
'blocklength_dist.py' - Plots distribution of block lengths (Plots)
'document_prediction.py' - Plots histogram of test set blocks and their labels. WARNING: Only use few documents
'confidence_analysis.py' - Visualization for fraction of high confidence blocks
'tensorboard_launch.py' - Launch tensorboard from stored model