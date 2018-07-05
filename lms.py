import argparse

#https://linuxconfig.org/how-to-use-argparse-to-parse-python-scripts-parameters#h4-conventions

if __name__ == '__main__':
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="Welcome to the わかりません help menu. \n © Copyright LMS., Inc., 1999 - 2005. All rights reserved."
    )
    
    parser.add_argument('mode', help="display, fetch")

    # Parse the arguments
    arguments = parser.parse_args()

    # Finally print the passed string
    print(arguments.mode)
