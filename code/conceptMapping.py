# Code for Concept Mapping in Python

class ConceptMapper():
    
    def __init__(self):
        pass 

    def checkRelativeLocation(self, locationDict: dict, ew_relation: str, ns_relation: str, searchTerm: str) -> bool:
        
        allConditionsSatisfied = False
        eastWestSatisfied = False
        northSouthSatisfied = False
        

        if ns_relation == "north_of" and ew_relation == None:
            if searchTerm in locationDict["northeast"] or searchTerm in locationDict["northwest"]:
                return True
        elif ns_relation == "north_of" and ew_relation == "west_of":
            if searchTerm in locationDict["northwest"]:
                return True
        elif ns_relation == "north_of" and ew_relation == "east_of":
            if searchTerm in locationDict["northeast"]:
                return True
            
        elif ns_relation == "south_of" and ew_relation == None:
            if searchTerm in locationDict["southeast"] or searchTerm in locationDict["southwest"]:
                return True
            
        elif ns_relation == "south_of" and ew_relation == "west_of":
            if searchTerm in locationDict["southwest"]:
                return True
        
        elif ns_relation == "south_of" and ew_relation == "east_of":
            if searchTerm in locationDict["southeast"]:
                return True
            
        elif ns_relation == None and ew_relation == "west_of":
            if searchTerm in locationDict["southwest"] or searchTerm in locationDict["northwest"]:
                return True
        
        elif ns_relation == None and ew_relation == "east_of":
            if searchTerm in locationDict["southeast"] or searchTerm in locationDict["northeast"]:
                return True
            
        else:
            return False

            