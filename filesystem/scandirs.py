""" Example of using scandir
Authors: Reinica and Nina"""
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument("-p", "--path", help="directory to start from", type=dir_path, default='.')
    return parser.parse_args()


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


def traverse(path):
    filesystem_list = []
    if not os.path.exists(path):
        return

    for f in os.scandir(path):
        path = os.path.join(path, f.name)
        filesystem_list.append(path)

    print(*filesystem_list, sep="\n")


def main():
    parsed_args = parse_arguments()

    if parsed_args.path:
        traverse(parsed_args.path)


# Execute
if __name__ == '__main__':
    main()
