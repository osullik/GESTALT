#System Imports
import random, json

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
        
        if self._MODE == "object_centric":
            print("\n\n= = = = = = = = =  OBJECT CENTRIC SEARCH = = = = = = = = = \n")

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
                result = self.CM.searchMatrix(conceptMaps[locationCM],searchOrder.copy())   #Don't forget to take a copy of the list... 
                if result == True: 
                    #print("\n", locationCM,"\n")
                    #print(conceptMaps[locationCM])
                    results.append(locationCM)
                    result = False
            
            if len(results) ==0:                                            #Output. TODO: Use Popup window to output
                print('No Results Found')
            else:
                print("Found Following Matches to Query:")
                for res in results: 
                    print(res)

        elif self._MODE == "location_centric":

            print("\n\n= = = = = = = = =  LOCATION CENTRIC SEARCH = = = = = = = = = \n")
            
            print("\nQuery Input:\n",query_df)
            jsonLocationsFile = "../data/output/concept_mapping/RelativeLocations_DBSCAN_PredictedLocations.JSON"
            
            
            queryLocations = self.CM.getRelativeLocation(self.placedObjects,
                                            (self.DEAD_CENTRE_X,self.DEAD_CENTRE_Y))

            with open(jsonLocationsFile, "r") as inFile:
                referenceLocations = json.load(inFile)

            locationHitCounter = {}
            for quadrant in queryLocations.keys():
                #print("QUADRANT",quadrant)
                for loc in referenceLocations:
                    for item in queryLocations[quadrant]:
                        if item in referenceLocations[loc][quadrant]:
                            try:
                                locationHitCounter[loc] +=1
                            except KeyError:
                                locationHitCounter[loc] = 1
                            #print(loc,"True")
                        else:
                            pass
                            #print(loc,"False")
            print("\nQuery Output:")
            for loc in locationHitCounter.keys():
                print(loc,locationHitCounter[loc])





        else:
            exit("UNKNOWN MODE, use object_centric or location_centric")

    def set_up_object_centric_search(self):
        self._MODE = "object_centric"
        self.prompt_frame.destroy()

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
                            text = 'GESTALT - OBJECT CENTRIC SEARCH',
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

        self.set_up_control_panel()


    def set_up_location_centric_search(self):
        self._MODE = "location_centric"
        self.prompt_frame.destroy()
        
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

        self.deadCentre = tk.Label(self.root,
                                    bg = '#ddcc99',
                                    text = "+",
                                    font = ('', 50))
        
        self.DEAD_CENTRE_X = (self.WIDTH*0.8)*0.5
        self.DEAD_CENTRE_Y = (self.HEIGHT*0.9)*0.5
        self.deadCentre.place(x= self.DEAD_CENTRE_X, y=self.DEAD_CENTRE_Y)


        self.set_up_control_panel()


        #Add title
        self.title = tk.Label(
                            bg = 'black',
                            fg = 'white',
                            text = 'GESTALT - LOCATION CENTRIC SEARCH',
                            font = ('', 30)
                        )
        self.title.place(x=5 , y=5)

        howTo = "In this mode, we assume you are estimating object positions relative to the CENTRE\of the location of interest. We assume that the map is oriented to the north (i.e. the top of the screen\nis north. To the best of your recollection, place out objects with where you remember\nthem in relation to that centre.)" 
        self.instructions = tk.Label(
                            bg = 'black',
                            fg = 'white',
                            text = howTo,
                            font = ('', 8)
                        )
        self.instructions.place(x=0 , y=self.HEIGHT-50)

        self.set_up_control_panel()


    def prompt_user_for_mode(self):

        self.prompt_frame = tk.Frame(self.root,                   #Frame for user to position search terms on
                                    bg='#aaaaaa', 
                                    width = self.WIDTH*0.25, 
                                    height = self.HEIGHT*0.25)
        self.prompt_frame.place(x =self.WIDTH*0.25, y = self.HEIGHT*0.5)

        self.btn_chooseLocMode = tk.Button( self.prompt_frame, 
                        width=20,
                        text = "Location-Centric Mode" , 
                        command = self.set_up_location_centric_search ).pack(side='top')

        self.btn_chooseObjMode = tk.Button( self.prompt_frame, 
                        width=20,
                        text = "Object-Centric Mode" , 
                        command = self.set_up_object_centric_search ).pack(side='bottom')

        

    def set_up_control_panel(self):
        #button to add a search term
        self.btn_addSearchTerm = tk.Button( self.root, 
                                width=10,
                                text = "Add Selected \nObject to Search" , 
                                command = self.show ).place(x=self.WIDTH-135,y=0.3*self.HEIGHT)

        #Button to execute the query
        self.btn_runQuery = tk.Button( self.root , 
                                width=10,
                                text = "Run Query" , 
                                #bg='green',
                                fg="green",
                                command = self.runQuery ).place(x=self.WIDTH-135,y=0.55*self.HEIGHT)

        #button to reset the interface
        self.btn_resetQuery = tk.Button( self.root , 
                                #bg= 'red',
                                width=10,
                                fg = 'red',
                                text = "RESET" , 
                                command = self.resetGUI ).place(x=self.WIDTH-135,y=0.8*self.HEIGHT)

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



if __name__=="__main__":

    #Init the inverted index to get access to its keys (the objects) which will be our search vocab. 
    II = InvertedIndex("../data/output/ownershipAssignment/DBSCAN_PredictedLocations_FT=0.0.csv")
    VOCAB = II.ii.keys()
    #print(VOCAB)

    GG = GestaltGUI(VOCAB)  # Initialise the Gestaly Gui
    GG.prompt_user_for_mode()


    
    


    GG.root.mainloop()

