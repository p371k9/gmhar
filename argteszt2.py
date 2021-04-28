import sys, os, logging, argparse
#import os
#import logging
#import argparse
parser = argparse.ArgumentParser(description='Process Google Maps HAR to .csv .')
parser.add_argument('har', type=argparse.FileType('r'), help='Input HAR file name for processing.')
parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout, help='If not specified, the output will be sent to STDOUT.')
parser.add_argument('--same', '-s', action="store_true", help='The name of the output file will be the same as the name of the input file, but with the extension .csv.')
args = parser.parse_args()
if args.same and args.outfile.name != '<stdout>':
    logging.error('outfile+same')
    exit()
if args.same:       
    if os.path.splitext(args.har.name)[1] == '.csv':
        #print("sfs")
        logging.error('Already has a .csv file extension!')
        exit()
    else:
        args.outfile = open(os.path.splitext(args.har.name)[0]+'.csv', 'w')         
with args.outfile as f:
    f.write(args.outfile.name)
    f.write("\n")
args.har.close() 
args.outfile.close()
