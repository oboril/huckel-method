# This script reads all .out files in specified folder, parses the data, and saves it as csv
# Run the script as:
# python parse.py [input folder] [output file]
# use the flag --full to include filenames and quotes
# use the flag --quotes to save the quotes only

import json
import os
import re
import logging
import sys
import numpy as np

logging.basicConfig(level=logging.INFO)

REGEX = {}

def initialize_regex():
    global REGEX

    REGEX["floating_number"] = re.compile(r"[\+-]?\d+\.\d+")

    REGEX["energy"] = re.compile(r"SCF Done:\s+E\(RHF\)\s+=\s*[\+-]?[\d\.]+(?=\s*A.U.)")
    REGEX["distance_matrix"] = re.compile(r"(?<=\n)\s*Distance matrix \(angstroms\):(.|\n)*?\n(?!\s*\d)")
    REGEX["quote"] = re.compile(r"(?<=\n\n\n)(.|\n)*?(?=\n\s*Job cpu time:)")
    REGEX["duplicate_spaces"] = re.compile(r"\ {2,}")


def parse_file(filepath):
    """
    Parses data from the given file.
    Parsed data include:
     - filename
     - distance and angle
     - SFC energy
     - quote
    """

    with open(filepath, 'r') as f:
        content = f.read()
    
    global REGEX
    results = {}

    temp = REGEX["energy"].search(content).group()
    temp = REGEX["floating_number"].search(temp).group()
    results["energy"] = float(temp)

    temp = REGEX["quote"].search(content).group()
    temp = temp.replace("\n","")
    temp = temp.strip()
    temp = REGEX["duplicate_spaces"].sub(" ", temp)
    results["quote"] = temp.replace(";",",")

    temp = REGEX["distance_matrix"].search(content).group()
    temp = REGEX["duplicate_spaces"].sub(" ",temp.strip())
    temp = temp.split("\n")[2:]
    temp = list(map(lambda x: x.strip().split(" "), temp))
    dist_XH = float(temp[1][2])
    dist_HH = float(temp[2][3])

    angle = np.arcsin(dist_HH/dist_XH/2)*2*180/np.pi
    results["distance"] = f"{dist_XH:0.4f}"
    results["angle"] = f"{angle:0.1f}"

    results["filename"] = filepath.split("/")[-1]

    return results

def process_folder(folder):
    # get all .out files in the folder
    files = [os.path.join(folder,f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f.endswith(".out")]

    logging.info(f"Discovered {len(files)} .out files")

    results = []
    for f in files:
        try:
            results.append(parse_file(f))
        except Exception as ex:
            logging.error(f"An error occured while parsing the file {f}. {ex}")

    return results

def data_to_table(data):
    table = [["filename","energy","distance","angle","quote"]]
    for d in data:
        table.append([d["filename"],d["energy"],d["distance"],d["angle"],d["quote"]])

    table = np.array(table)
    return table.astype(str)
    

if __name__ == '__main__':
    # Parse flags
    args = []
    full_output = False
    quotes_only = False
    for arg in sys.argv[1:]:
        if arg == "--full":
            full_output=True
        elif arg == "--quotes":
            quotes_only=True
        else:
            args.append(arg)

    # Parse input arguments
    if len(args) != 2:
        logging.error("Incorrect number of input arguments. Run this script as `python parse.py [input folder] [output file]`")
        exit(0)
    input_folder, output_file = args

    if not os.path.isdir(input_folder):
        logging.error(f"Invalid input folder '{input_folder}'")
        exit(0)
    
    # Process the data
    initialize_regex()

    data = process_folder(input_folder)

    data = data_to_table(data)

    # Save the data
    logging.info(f"Saving data to '{output_file}'")
    if quotes_only:
        # Save unique quotes, alphabetically sorted
        quotes = data[:,4]
        quotes = set(quotes)
        quotes = list(quotes)
        quotes = sorted(quotes)
        quotes = np.savetxt(output_file, quotes, fmt="%s")
    else:
        if not full_output:
            data = data[:,1:4]
        np.savetxt(output_file, data, delimiter=';', fmt="%s")

    logging.info("File saved, program exited successfuly")
    