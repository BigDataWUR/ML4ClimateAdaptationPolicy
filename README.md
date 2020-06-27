# ML4ClimateAdaptationPolicy
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/git/https%3A%2F%2Fgithub.com%2FBigDataWUR%2FML4ClimateAdaptationPolicy/master)  

Welcome to the git repository of **Machine learning for research on climate change adaptation policy integration: an explorative UK case study**  
It is important that you do not change the names of any folders  
or files before finishing the pipeline. 
Doing so, may raise errors as the scripts look in folders  
with these specific names.

Step 1:  
Download and extract PDF_files.zip in the root folder. Download here: doi: 10.5281/zenodo.3911168  
In the folder 'PDF_files' the following PDF documents are contained.  
'Adaptation policy documents' - Training data for adaptation policies  
'Mitigation policy documents' - Training data for mitigation policies  
'Non-climate policy documents' - Training data for non-climate documents  
'Mixed policy documents' - Testing data, any PDF document(s) you want to predict on.  
Step 2:  
In the folder 'Python Scripts' every script in the pipeline is contained.  
## MAIN PIPELINE  
'pdf_parser.py' - Extract raw text from PDf documents (parsed_files)  
'text_cleanup.py' - Filters, cleansand structurizes data into 'bags-of-words' (structured_files)  
'sqlite_db.py' - Builds database and inserts cleaned data (climate.db)  
'numberizer.py' - Builds vocabulary from training data (conversion_dictionary.txt)  
'TF_classification_BW.py' - Builds neural network and stores it (tensorflow/logdir)  
'TF_classification_predict.py' - Uses stored model to predict on new data. Results stored in database.  
## OPTIONAL  
'pipeline.py' - Runs every script in the main pipeline in order.  
'web_scraper.py' - Retrieves documents from gov.uk website (PDF_files\Scraped documents) -- OUTDATED  
'blocklength_dist.py' - Plots distribution of block lengths (Plots)  
'document_prediction.py' - Plots histogram of test set blocks and their labels. WARNING: Only use few documents  
'confidence_analysis.py' - Visualization for fraction of high confidence blocks  
'tensorboard_launch.py' - Launch tensorboard from stored model  