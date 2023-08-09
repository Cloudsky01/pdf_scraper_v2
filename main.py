import tabula
import pandas as pd
import os

TEMPLATE_PATH = "./template/template_1.json"


def openPDFTables(path):
    # Extract tables from the PDF into a list of DataFrames
    # Initialize variables to store extracted information
    tables = tabula.read_pdf_with_template(path, TEMPLATE_PATH, pages="all", encoding='ISO-8859-1')
    userInput = True
    for table in tables:
        for row in table.iterrows():
            while(userInput):
                print(row[1][0])
                print("Please enter if you want to keep the data or not")
                userInput = input()
                if(userInput == "yes"):
                    print("You have selected to keep the data")
                    break
                elif(userInput == "no"):
                    print("You have selected to remove the data")
                    break
                else:
                    print("Please enter a valid input")
        print(table.columns[0])
    return tables
    
# Function that iterate through the pdf directory
def main_sub_routine():
    directory = 'pdf'
    finalList = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        print("Opening file: {}".format(f))
        openPDFTables(f)
        break
        

if __name__ == '__main__':
    main_sub_routine()