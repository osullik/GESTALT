#System Imports
import random

#Library Imports
import tkinter as tk
import pandas as pd
import pickle

#User Imports

from conceptMapping import ConceptMapper
from search import InvertedIndex

# Global Vars:


#Initial Config

class GestaltGUI():

    def __init__(self, vocab:list):
        #Extract args to class properties
        self.VOCAB=vocab

        #Define window Constants
        self.HEIGHT=500
        self.WIDTH=700

        #Set up root window 
        self.root = tk.Tk()
        self.root.title('PictoralQuery')
        self.root.configure(bg='#FFFFFF')
        self.root.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.root.resizable(False, False)

        #Set up Frames
        self.top_frame = tk.Frame(self.root,                    #Frame to hold the header
                                    bg='#000000', 
                                    width=self.WIDTH, 
                                    height=self.HEIGHT*0.1)
        self.top_frame.place(x = 0, y = 0)

        self.left_frame = tk.Frame(self.root,                   #Frame for user to position search terms on
                                    bg='#ddcc99', 
                                    width = self.WIDTH*0.8, 
                                    height = self.HEIGHT*0.9)
        self.left_frame.place(x = 0, y = self.HEIGHT*0.1)

        self.right_frame = tk.Frame(self.root,                  # Control panel frame
                                    bg='#aacc99', 
                                    width = self.WIDTH*0.2, 
                                    height = self.HEIGHT*0.9)
        self.right_frame.place(x=self.WIDTH*0.8, y = self.HEIGHT*0.1)


        #Add title
        self.title = tk.Label(
                            bg = 'black',
                            fg = 'white',
                            text = 'GESTALT',
                            font = ('', 30)
                        )
        self.title.place(x=5 , y=5)

        howTo = "To search gestalt, please select from the items we know to be in the area using the dropdown. Once you have selected your term, please position it on the map. Assume that \nthetop of your screen is north. There is no particular reference point. Just place down any group of objects you can remember and drag them into different configurations. \nThe searching is on relative position, not exact, so you can be imprecise in your placement. \nWhen you aren't sure if an object was present, it is better to leave it out. After adding all terms, press the \"Run Query\" button to view your results" 
        self.instructions = tk.Label(
                            bg = 'black',
                            fg = 'white',
                            text = howTo,
                            font = ('', 8)
                        )
        self.instructions.place(x=0 , y=self.HEIGHT-50)

        # Objects
        self.placedObjects = {}                                     # Dict to track the objects placed by the user

        #Drop Down Menu
        self.clicked = tk.StringVar()
        self.DEFAULT_MSG = "Select Object"
        self.clicked.set(self.DEFAULT_MSG)
        
        # Create Dropdown menu
        self.drop = tk.OptionMenu( self.root, 
                                    self.clicked , 
                                    *self.VOCAB )                   # Where VOCAB is the keys for the inverted index
        self.drop.place(x = 0.8*self.WIDTH, y=0.1*self.HEIGHT)
        
    #FRONTEND FUNCTIONS:
    def show(self):                                                 # Adds a search term to the GUI, erroring if not valid
        if self.clicked.get() == self.DEFAULT_MSG:
            print("Please select an item from the list")
        else:
            cardID = self.createCard(self.clicked.get())
            self.placedObjects[cardID]["tk_object"].config( text = self.clicked.get() )

    def drag(self, event):                                          # Control the dragging of objects around
        event.widget.place(x=event.x_root, y=event.y_root,
                                            anchor="center")

    def resetGUI(self):                                             #Clearn out the riff raff, TODO: Implement per-object deletion
        for key in self.placedObjects.keys():                       #Destroy the objects
            (self.placedObjects[key]['tk_object']).destroy()

        del(self.placedObjects)                                     #Delete and reinitialise the placed object tracker. 
        self.placedObjects={}   

        del(self.flatDict)     
        del(self.CM)

    # BACKEND FUNCTIONS

    def createCard(self, objectName):                               #Card broadly used to mean 'object to place down"
        cardID = (len(self.placedObjects.keys())+1)                 #Create a unique id to track it
        if cardID in list(self.placedObjects.keys()):               #Enforce uniqueness
            while cardID in list(self.placedObjects.keys()):
                cardID +=1

        self.placedObjects[cardID] = {}                             #Build the entry to the dict.        
        self.placedObjects[cardID]["tk_object"] = tk.Label(self.root, bg='blue', text=objectName)
        self.placedObjects[cardID]["tk_object"].place(x=random.randint(200,400), y=random.randint(200,400),anchor="center")
        self.placedObjects[cardID]["tk_object"].bind("<B1-Motion>", self.drag)
        self.placedObjects[cardID]["name"] = objectName
        self.placedObjects[cardID]["predicted_location"] = "PICTORAL_QUERY"

        return(cardID)

    def runQuery(self):                                             #Execute the query on the set of locations
        for key in self.placedObjects.keys(): 
            self.placedObjects[key]["longitude"] = str(self.placedObjects[key]["tk_object"].winfo_rootx())
            self.placedObjects[key]["latitude"] = str(self.HEIGHT-self.placedObjects[key]["tk_object"].winfo_rooty()) #tkinter indexes from Top Left... 
        
        #print(self.placedObjects)

        self.flatDict = {}                                               #Flatten the dictrionary of objects into a dataframe
        self.flatDict["name"] = []
        self.flatDict["longitude"] = []
        self.flatDict["latitude"] = []
        self.flatDict["predicted_location"] = []
        for key in self.placedObjects.keys():
            self.flatDict["name"].append(self.placedObjects[key]['name'])
            self.flatDict["longitude"].append(self.placedObjects[key]['longitude'])
            self.flatDict["latitude"].append(self.placedObjects[key]['latitude'])
            self.flatDict["predicted_location"].append(self.placedObjects[key]['predicted_location'])
        query_df = pd.DataFrame.from_dict(self.flatDict,orient='columns')

        self.CM = ConceptMapper()                                          #Initialize a concept mapper
        queryMap = self.CM.createConceptMap(input_df=query_df, 
                                        inputFile=None)
        searchOrder = self.CM.getSearchOrder(queryMap['PICTORAL_QUERY'])
        #print("Search Order:",searchOrder)

        #Load in the pre-processed Concept maps for the locations using Pickle
        conceptMapFile = "../data/output/concept_mapping/ConceptMaps_DBSCAN_PredictedLocations.pkl"
        
        with open(conceptMapFile, "rb") as inFile:
            conceptMaps = pickle.load(inFile)
        
        results = []                                                    #Collate the results
        for locationCM in conceptMaps.keys():
            result = self.CM.searchMatrix(conceptMaps[locationCM],searchOrder)
            if result == True: 
                results.append(locationCM)
        
        if len(results) ==0:                                            #Output. TODO: Use Popup window to output
            print('No Results Found')
        else:
            print("Found Following Matches to Query:")
            for res in results: 
                print(res)


if __name__=="__main__":

    #Init the inverted index to get access to its keys (the objects) which will be our search vocab. 
    II = InvertedIndex("../data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv")
    VOCAB = II.ii.keys()
    #print(VOCAB)

    GG = GestaltGUI(VOCAB)  # Initialise the Gestaly Gui

    #button to add a search term
    GG.btn_addSearchTerm = tk.Button( GG.root, 
                            width=10,
                            text = "Add Selected \nObject to Search" , 
                            command = GG.show ).place(x=GG.WIDTH-135,y=0.3*GG.HEIGHT)

    #Button to execute the query
    GG.btn_runQuery = tk.Button( GG.root , 
                            width=10,
                            text = "Run Query" , 
                            #bg='green',
                            fg="green",
                            command = GG.runQuery ).place(x=GG.WIDTH-135,y=0.55*GG.HEIGHT)

    #button to reset the interface
    GG.btn_resetQuery = tk.Button( GG.root , 
                            #bg= 'red',
                            width=10,
                            fg = 'red',
                            text = "RESET" , 
                            command = GG.resetGUI ).place(x=GG.WIDTH-135,y=0.8*GG.HEIGHT)
    


    GG.root.mainloop()

