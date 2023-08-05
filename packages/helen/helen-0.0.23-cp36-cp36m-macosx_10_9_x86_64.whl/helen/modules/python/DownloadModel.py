import wget
import sys
import os
from helen.modules.python.FileManager import FileManager
from helen.modules.python.TextColor import TextColor


def download_models(output_dir):
    output_dir = FileManager.handle_output_directory(output_dir)
    sys.stderr.write(TextColor.YELLOW + "DOWNLOADING MODEL DESCRIPTION FILE" + TextColor.END + "\n")
    description_file = "https://storage.googleapis.com/kishwar-helen/models_helen/mp_helen_model_description.csv"
    wget.download(description_file, output_dir)
    sys.stderr.write("\n")
    sys.stderr.flush()

    with open(output_dir+'/mp_helen_model_description.csv') as f:
        models = [line.rstrip() for line in f]

    os.remove(output_dir+'/mp_helen_model_description.csv')

    for model in models:
        model_name, model_url = model.split(',')
        sys.stderr.write("INFO: DOWNLOADING FILE: " + str(model_name) + ".pkl\n")
        sys.stderr.write("INFO: DOWNLOADING LINK: " + str(model_url) + "\n")
        wget.download(model_url, output_dir)
        sys.stderr.write("\n")
        sys.stderr.flush()
