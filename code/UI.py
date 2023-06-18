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

    def __init__(self, vocab:list, objectList:list):
        #Extract args to class properties
        self.objectList = objectList
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
        self.top_frame = tk.Frame(self.root, 
                                    bg='#000000', 
                                    width=self.WIDTH, 
                                    height=self.HEIGHT*0.1)
        self.top_frame.place(x = 0, y = 0)

        self.left_frame = tk.Frame(self.root, 
                                    bg='#ddcc99', 
                                    width = self.WIDTH*0.8, 
                                    height = self.HEIGHT*0.9)
        self.left_frame.place(x = 0, y = self.HEIGHT*0.1)

        self.right_frame = tk.Frame(self.root, 
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

        # Objects

        self.placedObjects = {}

        #Drop Down Menu
        
        self.clicked = tk.StringVar()
        self.DEFAULT_MSG = "Select Object"
        self.clicked.set(self.DEFAULT_MSG)
        
        # Create Dropdown menu
        self.drop = tk.OptionMenu( self.right_frame , self.clicked , *self.VOCAB )
        self.drop.pack(side = "top")
        
    #FRONTEND FUNCTIONS:

    def show(self):
        if self.clicked.get() == self.DEFAULT_MSG:
            print("Please select an item from the list")
        else:
            cardID = self.createCard(self.clicked.get())
            self.placedObjects[cardID]["tk_object"].config( text = self.clicked.get() )

    def drag(self, event):
        event.widget.place(x=event.x_root, y=event.y_root,anchor="center")


    def resetGUI(self):
        self.left_frame.destroy()
        self.left_frame = tk.Frame(self.root, 
                                    bg='#ddcc99', 
                                    width = self.WIDTH*0.8, 
                                    height = self.HEIGHT*0.9)
        self.left_frame.place(x = 0, y = self.HEIGHT*0.1)

        for key in self.placedObjects.keys():
            print(key)
            label.destroy(placedObjects[key]['tk_object'])

        del(self.placedObjects)

        self.placedObjects={}        

    # BACKEND FUNCTIONS

    def createCard(self, objectName):
        #Generate a key for the objects
        #print("clicked", self.clicked.get())
        cardID = (len(self.placedObjects.keys())+1)
        print("Card ID is:", cardID)
        if cardID in list(self.placedObjects.keys()):
            while cardID in list(self.placedObjects.keys()):
                cardID +=1
        self.placedObjects[cardID] = {}        
        self.placedObjects[cardID]["tk_object"] = tk.Label(self.root, bg='blue', text=objectName)
        self.placedObjects[cardID]["tk_object"].place(x=random.randint(200,400), y=random.randint(200,400),anchor="center")
        self.placedObjects[cardID]["tk_object"].bind("<B1-Motion>", self.drag)
        self.placedObjects[cardID]["name"] = objectName
        self.placedObjects[cardID]["predicted_location"] = "PICTORAL_QUERY"

        return(cardID)

    def runQuery(self):
        for key in self.placedObjects.keys(): 
            self.placedObjects[key]["longitude"] = str(self.placedObjects[key]["tk_object"].winfo_rootx())
            self.placedObjects[key]["latitude"] = str(self.HEIGHT-self.placedObjects[key]["tk_object"].winfo_rooty()) #tkinter indexes from Top Left... 
        
        #print(self.placedObjects)

        flatDict = {}
        flatDict["name"] = []
        flatDict["longitude"] = []
        flatDict["latitude"] = []
        flatDict["predicted_location"] = []
        for key in self.placedObjects.keys():
            flatDict["name"].append(self.placedObjects[key]['name'])
            flatDict["longitude"].append(self.placedObjects[key]['longitude'])
            flatDict["latitude"].append(self.placedObjects[key]['latitude'])
            flatDict["predicted_location"].append(self.placedObjects[key]['predicted_location'])
        query_df = pd.DataFrame.from_dict(flatDict,orient='columns')

        #print(query_df)

        CM = ConceptMapper()
        queryMap = CM.createConceptMap(input_df=query_df, inputFile=None)
        searchOrder = CM.getSearchOrder(queryMap['PICTORAL_QUERY'])
        print("Search Order:",searchOrder)

        conceptMapFile = "../data/output/concept_mapping/ConceptMaps_DBSCAN_PredictedLocations.pkl"
        
        with open(conceptMapFile, "rb") as inFile:
            conceptMaps = pickle.load(inFile)
        
        results = []
        self.result_message = "No Results Found"


        for locationCM in conceptMaps.keys():
            result = CM.searchMatrix(conceptMaps[locationCM],searchOrder)
            if result == True: 
                results.append(locationCM)
        
        if len(results) ==0:
            print('No Results Found')
        else:
            print("Found Following Matches to Query:")
            for res in results: 
                print(res)

    



if __name__=="__main__":

    II = InvertedIndex("../data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv")
    VOCAB = II.ii.keys()
    print(VOCAB)

    

    GG = GestaltGUI(VOCAB,["tree", "bench", "table"])

    #for obj in GG.objectList:
    #    GG.createCard(obj)

    # Create button, it will change label text
    GG.btn_addSearchTerm = tk.Button( GG.right_frame , 
                            text = "Add Selected \nObject to Search" , 
                            command = GG.show ).pack(side="top")

    GG.btn_resetQuery = tk.Button( GG.right_frame , 
                            #bg= 'red',
                            fg = 'red',
                            text = "RESET" , 
                            command = GG.resetGUI ).pack(side="bottom")


    GG.btn_runQuery = tk.Button( GG.right_frame , 
                            text = "Run Query" , 
                            #bg='green',
                            fg="green",
                            command = GG.runQuery ).pack(side="bottom")


    GG.root.mainloop()

