#!/usr/bin/env python

import argparse
from tpextract import read_topas, extract_big_out, extract_refined, extract_sequential, topas_to_csv


def main():

    parser = argparse.ArgumentParser(description="Topas Extractor is a tool for extracting refined paramters from Topas .OUT files.")
    parser.add_argument('topas-out', type=str, help="Path to the Topas .OUT file.")
    parser.add_argument('output', type=str, help="Output filename. Name of your results file.")

    parser.add_argument(
        "-exc",
        type=str, 
        help="""Parameters to exclude from Topas OUT file. Written as a comma separated list:
                E.g: c, a, scale, ...""")
    parser.add_argument(
        "-sct",
        type=str,
        help="""Parameters to select specifically from Topas OUT file. Written as a comma
                separated list. 
                E.g.: c, a, b, ....""")

    parser.add_argument('-big', action="store_true", help="For surface or parametric refined BIG.OUT Topas files.")
    parser.add_argument('-seq', action="store_true", help="For sequential refinement of a folder of Topas OUT files.")
    parser.add_argument('-xdd', action="store_true", help="Include the xdd file name in the extraction.")
    parser.add_argument('-delim', type=str, default="xdd", help="Topas .OUT page divider/delimiter. Defaults to \"xdd\".")
    


    args = parser.parse_args()
    args_dict = vars(args)

    if args_dict['exc']:
        exclude = [p for p in args_dict['exc'].split(',')]
    else:
        exclude = []

    if args_dict['sct']:
        select = [p for p in args_dict['sct'].split(',')]
    else:
        select = []
    
    

    if args_dict['big']:
        tp_text = read_topas(args_dict['topas-out'])
        params = extract_big_out(
                text=tp_text,
                select=select,
                exclude=exclude,
                xdd_include=args_dict['xdd'],
                delim=args_dict['delim'])

    elif args_dict['seq']:
        params = extract_sequential(
                folder=args_dict['topas-out'],
                select=select,
                exclude=exclude
        )

    else:
        tp_text = read_topas(args_dict['topas-out'])
        params = extract_refined(
                text=tp_text,
                select=select,
                exclude=exclude,
                xdd_include=args_dict['xdd'])

    topas_to_csv(params=params, output=args_dict['output'])

    return

if __name__ == "__main__":
    main()
