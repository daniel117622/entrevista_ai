## Usage : 
    - Install dependencies using the requirements.txt file
    - Run the main.py file.
    - Select the driver to use, both will run in headless mode for better confort.
    - Navigate the menu to select a feature to extract
    - Select the outfile name and wait for it to be written

## Description:
This program uses selenium headless webdrivers to extract information from an static website. The programs makes uses of types for safer development. 

dataformat.py : This file declares the schemas of the data used in the mexico driver and the united states driver. This is crucial to ensure all the other classes know which properties are accessible while building the datastructures in memory, and while writing the excel files.

datawriter.py : Uses pandas library and openpyxl engine to get an object and convert it into an excel file. For mexico a dictionary structure is used, this has the advantage of being closely related to JSON objects which are commonly used in web development. Then the united states uses Lists of Dataclasses to write to excel, this makes the process quite straightforward as each Dataclass represents a single entry for the pandas library.

mexico.py , unitedstates.py : This classes perform the core tasks of getting the data out of the DOM with selenium. The driver is an injected depency, this can make the class more reusable with different driver interfaces. Also in the mexico class there is a method which attempts to retrieve data from different URL's concurrently. This was not successful as it took more time than the single-threaded approach. It was determined that the time bottleneck was in the data retrieval and not in the network requests.

ipynb files : This files were used during development to carefully determine the data structures retrieved from the DOM. Careful consideration was taken while choosing the correct data structures and error handling was taken into consideration by using default_dicts and default values for the dataclasses

## Further considerations: 
The GUI of the program is quite simple. It could be improved with tkinter or other GUI frameworks. Also the program could later write to different sheets of the same Excel files. To create better looking excel files, I was planning in using openpyxl directly to apply styles and cell-fitting methods for the final files. 




    