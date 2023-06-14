# Code for Search in Gestalt

import pandas as pd
import glob
import os
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion

class InvertedIndex:
    """
    """
    def __init__(self, filename):
        self.objects_df = pd.read_csv(filename)[['name','predicted_location']]
        self.objects_df_grouped = self.objects_df.groupby(self.objects_df.columns.tolist(),as_index=False).size()
        self.objects_df_grouped = self.objects_df_grouped.rename(columns={'size':'num_occurences'})
        self.objects_df_grouped_list = pd.DataFrame(self.objects_df_grouped.groupby('name')['predicted_location'].apply(list))
        self.__make_ii__()
    def __make_ii__(self):
        self.ii = dict()
        for idx, row in self.objects_df_grouped_list.iterrows():
            self.ii[idx] = set(row['predicted_location'])
    
    def search(self, arg):                      #if want to use a string list of input terms change line to: def search(self, *arg):
        set_list = [self.ii[x] for x in arg]
        return set.intersection(*set_list)

#class SearchCompleter(Completer):
#    def __init__(self, inverted_index: InvertedIndex):
#        self.inverted_index = inverted_index
#    def get_completions(self, document, complete_event):
#        if complete_event.completion_requested:
#            for match in self.inverted_index.search(document.text):
#                yield Completion(match.ljust(document.cursor_position), start_position=-document.cursor_position)
                
                
#def main():
#    directory_name = os.getcwd()
#    objects_file = "data/output/ownershipAssignment/DBSCAN_PredictedLocations.csv"
#    filename = glob.glob(os.path.join(directory_name, objects_file))[0]
#    inverted_index = InvertedIndex(filename)
    #print(inverted_index.search('apple','wine_barrell'))
    #user_input = prompt("> ", completer=SearchCompleter(inverted_index), complete_while_typing=True)
#    print(inverted_index.search("person", "picnic_table"))
#if __name__ == "__main__":
#    main()