import pathlib
import sys

import plfatools

def main():
    """Reads files in dir specified in first argument and writes a formatted file named "final.csv" to dir specified in second argument"""
    if len(sys.argv) == 3:
        aggregator = plfatools.Aggregator()
        
        # Cast the first argument to a Path type
        dir_path = pathlib.Path(sys.argv[1]) 
        
        # Add in the name of the file to end of output path
        output_path = pathlib.Path(str(sys.argv[2]), 'final.csv') 
        
        # Aggregate
        final = aggregator.read_dir(dir_path) 
        
        # Output excel file to path specified
        final.to_csv(output_path, index=False)

    else:
        print('Please specify an input directory and an output directory')

if __name__ == "__main__":
    main()