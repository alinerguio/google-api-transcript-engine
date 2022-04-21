# Google Cloud Speech API usage for Portuguese

## Goal

The goal is to download and process audios to be able to transcript them using the google transcript tool. To use this script, your audios must be in brazilian portuguese (if not using the indicated) or you must change the script *main.py* where there are the "language_code" configuration - [possible options](https://cloud.google.com/speech-to-text/docs/languages).

## Requirements

To use this code, you'll need this requirements.   

[![Python Version](https://img.shields.io/badge/python-3.8.2-green)](https://www.python.org/downloads/release/python-382/)

When the repository is first cloned, use this commands:
```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Execution
Then, every time you want to access, don't forget to activate you enviroment:
```
$ source env/bin/activate
```

## Tutorial

For the understandig of the usage of the tool, the following [tutorial](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries?authuser=1) was used. In this tutorial, other than initiate your understanding of the platform, you will find how to creat a key file (in json format) that you will need to rename as "key-file.json" in order to use it. 

## Pipeline

### Downloading and Processing Data

Check [this repository](https://github.com/alinerguio/processing-data) for more info on this matter.  

### Transcribing

The main objective of this repository is to use the google cloud platform and its tool of transcription, focused on Brazilian Portuguese. This script requires the **key-file.json** already mentioned, the path to the info file (dictionary saved in txt mentioned in the last session). There are three main functions in this script: 

 - **upload_files**: upload the files to the bucket. 
 - **transcript_files_txt**: transcript the files in the bucket and saves the trascription in a txt file or
 - **transcript_files_dataset**: transcript the files in the bucket and saves the trascription in a dataframe.
 - **delete_folder**: delete the folder where the files are in the bucket.

The transcription is saved as a csv file, in a dataframe format having two columns: trascription and name file.

## Executing scripts

To execute the scripts, there is the need to set the environment - as stated in the "Requirements" session. After that, is also essential that the data is processed as described previously (Downloading and Processing Data). To execute the code, is only necessary to execute the python command and the script name, as ilustrated below:

```
$ python3 main.py
```

