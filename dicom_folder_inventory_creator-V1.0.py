###Author: Saeed Arbabi 12/1/2019
### this code aims to give me an overview of all the DICOM files I have in a folder and it's subfolders organized in a CSV file
#pass your main DICOM data folder to the program as a command line argument

import glob, os, sys
import SimpleITK as sitk
import numpy as np

###step1: find all the dicom series in the data directory and subdirectories
DATA_DIR = sys.argv[1]
print(DATA_DIR)
dicom_folders = {}
for root, dirs, files in os.walk(DATA_DIR):
    for file in files:
        if file.endswith(".dcm"):
            if(root not in dicom_folders):
                dicom_folders[root]=1
            else:
                dicom_folders[root]+=1

###step2: read each dicom serie and extract info about it from dicom tags and save in CSV file
tags_to_copy = ["0010|0010",  # Patient Name
                "0008|0020",  # Study Date
                "0008|0030",  # Study Time
                #"0008|0050",  # Accession Number
                "0008|0060",  # Modality
                "0018|0015",  # Body Part Examined
                "0008|103e",   # Series Description
                "0018|0050", # Slice Thickness
                "0028|0030" # Pixel Spacing
                ]
data_array = np.empty((0, 10), str)
data_array = np.append(data_array, np.array([["patientId", "studyDate", "studyTime", "modality", "bodyPart", "description/sequence", "sliceThickness", "pixelSpacing", "numSlices", "dicomFolder"]]), axis=0)

for dicom_folder, num_slices in dicom_folders.items():
    reader = sitk.ImageFileReader()

    print(glob.glob(f"{dicom_folder}/*.dcm")[0])
    reader.SetFileName(glob.glob(f"{dicom_folder}/*.dcm")[0])
    reader.LoadPrivateTagsOn();

    try:
        reader.ReadImageInformation();
    except:
        continue

    existing_keys = reader.GetMetaDataKeys()
    tags_array = np.empty(0, str)
    for k in tags_to_copy:
        if(k in existing_keys):
            v = reader.GetMetaData(k)
        else: v="-"
        tags_array = np.append(tags_array, v)

    tags_array = np.append(tags_array, num_slices)
    tags_array = np.append(tags_array, dicom_folder)

    data_array = np.append(data_array, np.array([tags_array]), axis=0)

np.savetxt(f"{DATA_DIR if DATA_DIR.endswith('/') else DATA_DIR+'/' }data_inventory.csv", data_array, delimiter=',', fmt='%s')
