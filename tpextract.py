import os 
import re
import pandas as pd

def read_topas(tpfile):
    """Reads the TOPAS .OUT file.

    Args:
        tpfile (str): Path to the topas .OUT file.

    Raises:
        ValueError: If path to the tpfile does not lead to a file. 
        ValueError: If the tpfile is not a TOPAS file.

    Returns:
        (str): Read topas .OUT file as a string.
    """

    # CHECKING IF THE FILE IS A VALID TOPAS FILE
    if not os.path.isfile(tpfile):
        raise ValueError(f"{tpfile} is not a valid file.")

    if not tpfile.endswith((".out", ".inp")):
        print(tpfile)
        print(tpfile.endswith(".inp"))
        raise ValueError(f"\"{tpfile}\" is not a Topas file.")

    #topas_specific = ['local', 'site']  # Topas keywords which require special treatement

    # READING FILE
    file = open(tpfile, 'r')
    text = file.readlines()
    file.close()

    return text


def extract_refined(text,  exclude=[], select=[], xdd_include=True):
    """[summary]

    Args:
        text (str): Read in Topas .OUT file, via topas_read()
        exclude (list, optional): List of parameters to exclude from the extraction.
        select (list, optional): List of parameters to exclusivly select from the extraction.
        xdd_include (bool, optional): To include the xdd file name. Defaults to True.

    Returns:
        dict: Extracted topas parameters as a dict.
    """

    ## GATHERING REFINED DATA
    found_params = {}  # Empty dict
    i = 0
    for line in text:

        # GETTING THE XDD FILE NAME
        if xdd_include:
            if re.search(r"^(?:\s{0,100})xdd", line):  # Getting the xdd file
                value = re.findall(r'(?<=xdd ).+', line)[0]
                if len(value.split("\\")) > 0:
                    found_params['xdd'] = [value.split("\\")[-1]]
                else:
                    found_params['xdd'] = [value]
                
                i += 1  

        # GETTING THE REFINED PARAMETERS
        if re.search(r"(?<=\s|-)[\d.]+(?=`)", line):  # Check if line contains a refined parameter

            key = re.findall(r"^(?:[\t\s]{0,100})[\w_\d]+", line)  # We get the first word of the line
            
            if len(key) == 0: #  if we don't get a match we assign "unknown_#"
                key = f"unknown_{len(found_params)-1}"
            else:
                key = key[0] 
            
            if re.search(r"local|site", key):  # Here we check if the key contains local or site.
                key = re.findall(fr"(?<={key})(?:[\s]+)[\w]+", line)[0]  # We take the word after (local or site)

            key = re.findall(r"\w+", key)[0]  # Our final key
            value = re.findall(r"[e\d.-]+(?=`)", line)  # The refined value
            value = [float(val) for val in value] # Converting to float.

            if key in found_params.copy().keys():
                repeating_key = len([p for p in found_params.keys() if key in p]) + 1
                if repeating_key == 2:
                    
                    old_val = found_params[key]
                    key_old = key + f'_01'
                    print(f"old key: {key_old}")
                    found_params[key_old] = old_val
                    del found_params[key]

                if repeating_key < 99:
                    key = key + f'_{repeating_key:02}'
                else:
                    key = key + f'_{repeating_key:03}'
                
                print(f"regular key {key}")

            found_params[key] = value

    ## SPLITTING PARAMETERS WITH SEVERAL REFINED VALUES
    old_params = found_params.copy()  # We need to copy the dict to delete keys itterable.
    for key in old_params.keys():
        if len(old_params[key]) > 1:
            for i, val in enumerate(old_params[key]):
                new_key = key + f'_{i+1:02}'

                found_params[new_key] = [val]

            del found_params[key]

    # EXCLUDING/SELECTING PARAMETERS

    if select:
        select_params = {}
        for sel in select:
            
            for param_lbl in found_params.keys():
                if re.search(fr"^{sel}", param_lbl):
                    val = found_params[param_lbl]
                    select_params[param_lbl] = val

        if exclude:
        
            for exl in exclude:
                for param_lbl in select_params.copy().keys():
                    if re.search(fr"^{exl}", param_lbl):
                        
                        del select_params[param_lbl]

        return select_params
    
    if exclude:
        for exl in exclude:
            for param_lbl in found_params.copy().keys():
                if re.search(fr"^{exl}", param_lbl):
                    del found_params[param_lbl]
    return found_params


def extract_big_out(text, exclude=(), select=(), xdd_include=True):
    """Extracts refined parameters from BIG.OUT Topas files, generated
    typically from surface refinements:

    https://github.com/Topas-Nordic

    Args:
        text (str): Read in Topas .OUT file, via topas_read()
        exclude (list, optional): List of parameters to exclude from the extraction.
        select (list, optional): List of parameters to exclusivly select from the extraction.
        xdd_include (bool, optional): To include the xdd file name. Defaults to True.

    Returns:
        dict: Extracted topas parameters as a dict.
    """

    # FINDING NUMBER OF FILES AND SECTION LENGTS
    sep = []
    for i, line in enumerate(text):
        if re.search(r"xdd", line):
            sep.append(i)

    number_files = len(sep)
    sep = [s - sep[0] for s in sep]

    j, k = 0, 1
    for i in range(0, number_files):
        if k == number_files:
            wanted_text = text[sep[j]:]
            found_params = extract_refined(text=wanted_text, exclude=exclude, select=select, xdd_include=xdd_include)
            break
        
        else:
            wanted_text = text[sep[j]:sep[k]]
            found_params = extract_refined(text=wanted_text, exclude=exclude, select=select, xdd_include=xdd_include)
            if i == 0:
                main_params = found_params
            else:
                for key in found_params.keys():
                    vals = found_params[key]
                    main_params[key].append(vals[0])

        j += 1
        k += 1

    return main_params

def topas_to_csv(params, output=None):
    """Function which exports the extracted parameters as .csv

    Args:
        params (dict): Dictionary with extracted refined parameters.
        output (str, optional): Output path and file name. E.g. output.csv
    """

    if output:
        filename = f"{output}"
    else:
        filename = "topas_results.csv"

    df = pd.DataFrame(params)
    df.to_csv(filename)
