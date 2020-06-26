#!usr/bin/env/python
"""
Author: Shashi
Description: Main pipeline. Wrappper for the other functions in this folder.
"""

import os
from subprocess import Popen, PIPE, STDOUT


def run_script(script_name):
    """Runs a single python 3 script through cmd

    script_name: string, name of the python script to be run
    """
    cmd = "py -3 "+script_name
    proc = Popen(cmd.split(' '), stdout=PIPE, stderr=PIPE)
    output, error = proc.communicate()
    if output:
        print(output)
    if error:
        print(error)
    
if __name__ == '__main__':
    print('Starting pipeline ...')
    #May sometimes give error, if it does, re-launch pipeline
    run_script('pdf_parser.py')
    print('PDF files parsed and stored in parsed_files')
    run_script('text_cleanup.py')
    print('Cleaned and structured text files stored in structured_files')
    run_script('sqlite_db.py')
    print('climate.db sucessfully made')
    run_script('numberizer.py')
    print('conversion_dictionary.txt sucessfully made')
    run_script('TF_classification_BW.py')
    print('Model sucessfully built')
    run_script('TF_classification_predict.py')
    print('Predictions added to the database')
