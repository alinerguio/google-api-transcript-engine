import os
import ast
import json
import sys
import datetime

from google.cloud import speech
from google.cloud import storage

import pandas as pd


def log_time_specifics(start_time, end_time, dataset, quantity_files):
    process_time = end_time - start_time

    if os.path.isfile('execution_time_specifics.txt'):
        f = open('execution_time_specifics.txt', 'a')
    else:
        f = open('execution_time_specifics.txt', 'w')
        
    f.write('\n' + dataset + ';' +  str(quantity_files) + ';' + str(process_time))
    f.close()


def iterate_folder(speech_client, storage_client, main_dir, bucket_name):
    all_folders = [folder for folder in os.listdir(main_dir) if '.' not in folder]
    
    for folder in all_folders:
        start_time = datetime.datetime.now()
        quantity_files = 0 

        curr_dir = main_dir + folder
        transc_folder = []

        all_files = [file for file in os.listdir(curr_dir) if '.wav' in file]

        if not(os.path.isdir('./transcriptions/')):
            os.mkdir('./transcriptions/')

        output_path = './transcriptions/' + folder + '.csv'

        if os.path.isfile(output_path):
            files_transcripted = pd.read_csv(output_path)
            files_transcripted_list = files_transcripted.file.tolist()
            all_files = [file for file in all_files if file not in files_transcripted_list]

        for file in all_files:
            try:
                resp = transcribe(speech_client, storage_client, curr_dir + '/' + file, folder, bucket_name)

                final_result = pd.DataFrame([{'transcriptions': resp, 'file': file, 'database': folder}])
                final_result.to_csv(output_path, mode='a', header=not os.path.exists(output_path))

            except Exception as e:
                print('Not possible to proceed to transcript file: ' + file)
                print(e)

            except KeyboardInterrupt:
                print('\nKeyboardInterrupt: stopping manually')
                end_time = datetime.datetime.now()
                log_time_specifics(start_time, end_time, folder, quantity_files)

                sys.exit()

        end_time = datetime.datetime.now()
        log_time_specifics(start_time, end_time, folder, quantity_files)


def delete_folder(storage_client, folder_name, bucket_name):
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(folder_name)
    blobs = bucket.list_blobs(prefix=folder_name)
    for blob in blobs:
      blob.delete()

    print("{} deleted.".format(folder_name))


def upload_files(storage_client, file, bucket_name):
  bucket = storage_client.get_bucket(bucket_name) # name of the bucket

  blob = bucket.blob(file)
  blob.upload_from_filename(file)
  print("{} uploaded.".format(file))


def transcribe_file(client, file, bucket_name):
  gcs_uri = "gs://" + bucket_name + "/" + file  # name of the bucket + file already uploaded 

  audio = speech.RecognitionAudio(uri=gcs_uri)

  config = speech.RecognitionConfig(
      encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
      language_code="pt-BR",
  )

  response = client.recognize(config=config, audio=audio)

  return response


def transcribe(speech_client, storage_client, local_file, folder, bucket_name):
    upload_files(storage_client, local_file, bucket_name)
    resp = transcribe_file(speech_client, local_file, bucket_name)
    delete_folder(storage_client, folder, bucket_name)

    return resp


def log_time(start_time, end_time):
    process_time = end_time - start_time

    if os.path.isfile('execution_time.txt'):
        f = open('execution_time.txt', 'a')
        f.write('\n' + str(process_time))
        f.close()
    else:
        f = open('execution_time.txt', 'w')
        f.write(str(process_time))
        f.close()


if __name__ == '__main__':
    main_dir = '../data/'
    bucket_name = 'transcricao-pt-br'
    key_path = None

    if key_path == None:
        if len(sys.argv) != 2:
            print('usage: python ' + sys.argv[0] + ' <google-cloud-key-json-path>')
            exit(1)
        key_path = sys.argv[1]

    start_time = datetime.datetime.now()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_path

    storage_client = storage.Client()
    speech_client = speech.SpeechClient()

    try:
        iterate_folder(speech_client, storage_client, main_dir, bucket_name)
        end_time = datetime.datetime.now()
        log_time(start_time, end_time)
    except Exception as e:
        end_time = datetime.datetime.now()
        log_time(start_time, end_time)
        print(e)
