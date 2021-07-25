import os
import sys
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument("-p", "--path", help="directory to start from", type=dir_path, default='.')
    return parser.parse_args()

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

def createtree(path):
    path = path.rstrip(os.sep)
    start = path.count(os.sep)
        
    for root, dirs, files in os.walk(path):
        current = root.count(os.sep)
        actual = current - start
        spacing = (actual) * ' '
        filesystem_list = [file for file in files]
        sys.stdout.write(spacing + '-' + os.path.basename(root) + ' ' +
                         str(filesystem_list) + '\n')

def main():
    parsed_args = parse_arguments()
    print(parsed_args)

    if parsed_args.path:
        createtree(parsed_args.path)

# Execute
if __name__ == '__main__':
    main()





