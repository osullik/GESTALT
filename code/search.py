# Code for Search in Gestalt

import pandas as pd
from collections import OrderedDict

def normalize_object_term(term):
    # TODO implement fuzzy term matching with OSM API
    return term

class InvertedIndex:
    """
    """
    def __init__(self, filename=None, dataframe=None):
        if filename is not None:
            self.df = pd.read_csv(filename)
        else:
            self.df = dataframe
        self.objects_df = self.df[['name','predicted_location']]
        self.objects_df_grouped = self.objects_df.groupby(self.objects_df.columns.tolist(),as_index=False).size()
        self.objects_df_grouped = self.objects_df_grouped.rename(columns={'size':'num_occurences'})  # this puts object counts in there, but we drop it for now
        self.objects_df_grouped_list = pd.DataFrame(self.objects_df_grouped.groupby('name')['predicted_location'].apply(list))
        self.__make_ii__()
        self.__make_adj__()

    def __make_ii__(self):
        self.ii = dict()
        self.ii_counter = dict()
        for idx, row in self.objects_df_grouped_list.iterrows():
            self.ii[idx] = set(row['predicted_location'])
            self.ii_counter[idx] = len(set(row['predicted_location']))

    def getIndex(self):
        return self.ii
    
    def getIndexCounter(self):
        return self.ii_counter

    def most_discriminative(self, query_terms):
        best_qt = query_terms[0]
        for qt in query_terms:
            if self.ii_counter[qt] < self.ii_counter[best_qt]:
                best_qt = qt
        return best_qt

    def __make_adj__(self):
        self.df['prob'] = self.df['object_prob'] * self.df['assignment_prob']
        self.adj = self.df.groupby(['name','predicted_location'], as_index=False).agg({'prob':'max'})
        return self.adj


    def get_prob(self, Loc : str, Obj : str):
        return self.adj[(self.adj['name'] == Obj) & (self.adj['predicted_location'] == Loc)]['prob'].item()


    def rank(self, Locs : set, Objs : set):
        loc_ranks = OrderedDict()
        for L in Locs:
            p = 1
            for Ob in Objs:
                p *= self.get_prob(L, Ob)
            loc_ranks[L] = p
        return sorted(loc_ranks, key=loc_ranks.get, reverse=True)

    def __search__(self, query_terms : list):
        try:
            set_list = [self.ii[normalize_object_term(x)] for x in query_terms]
            return set.intersection(*set_list)
        except KeyError:
            print("Not found in the database")

    def search(self, query_terms : list):
        try:
            set_list = [self.ii[normalize_object_term(x)] for x in query_terms]
            return list(set.intersection(*set_list)), query_terms
        except KeyError:
            print("Not found in the database")
        

    def ranked_search(self, query_terms : list):
        try:
            set_list = [self.ii[normalize_object_term(x)] for x in query_terms]
            return self.rank(set.intersection(*set_list), query_terms), query_terms
        except KeyError:
            print("Not found in the database")

    def fuzzy_search(self, query_terms : list):
        # Assume inverted index of object_class -> {Locations} exists
        s = self.__search__(query_terms)
        if not s:
            return s, query_terms
        if len(s) == 0:
            q = []
            while True:  # TODO make this cleaner and check end conditions
                best_qt = self.most_discriminative(query_terms)
                q.append(best_qt)
                query_terms.remove(best_qt)
                s = self.__search__(q)
                if len(s) > 0:
                    continue
                else:  # went too far, adding one too many search terms
                    q.pop()  # Remove most recent
                    s = self.__search__(q)  # Rerun to get nonempty result
                    query_terms = q
                    break
        if len(s) > 1:
            self.rank(s, query_terms)
        return s, query_terms  # returns query_terms since they may be a reduces subset of original query terms
     
                
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