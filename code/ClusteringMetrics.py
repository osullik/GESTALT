import Levenshtein
import pandas as pd
import numpy as np
import argparse


class ClusteringMetrics:
    def __init__(self, object_assignment_filename):
        self.metrics_df = pd.read_csv(object_assignment_filename)[['ground_truth_location','predicted_location']].copy()
        self.metrics_df.loc[:,'TP'] = self.metrics_df.apply(lambda row : Levenshtein.ratio(row['ground_truth_location'], row['predicted_location']) >= 0.7 , axis=1)
        self.metrics_df.loc[:,'F_'] = self.metrics_df.apply(lambda row : Levenshtein.ratio(row['ground_truth_location'], row['predicted_location']) < 0.7 , axis=1)

    def clustering_recall(self):
        TP_dict = dict()
        FN_dict = dict()
        recall_dict = dict()

        true_locs_list = ['Ali\'s Vineyard', 'Little River Winery and Café', 'Faber Vineyard', 'Ugly Duckling Wines', 'Oakover Grounds', 'Lancaster Wines']

        for vineyard in true_locs_list:
            select_df = self.metrics_df[self.metrics_df['ground_truth_location'] == vineyard].drop_duplicates()
            TP_dict[vineyard] = len(select_df[select_df['TP'] == True])
            FN_dict[vineyard] = len(select_df[select_df['F_'] == True])

        for vineyard in TP_dict.keys():
            recall = TP_dict[vineyard] / (TP_dict[vineyard] + FN_dict[vineyard])
            recall_dict[vineyard] = recall
            class_size = TP_dict[vineyard] + FN_dict[vineyard]

        avg_recall = np.mean(list(recall_dict.values()))

        return avg_recall, recall_dict

    def clustering_weighted_recall(self):
        TP_dict = dict()
        FN_dict = dict()
        weighted_recall_dict = dict()
        total_dict = dict()

        true_locs_list = ['Ali\'s Vineyard', 'Little River Winery and Café', 'Faber Vineyard', 'Ugly Duckling Wines', 'Oakover Grounds', 'Lancaster Wines']

        for vineyard in true_locs_list:
            select_df = self.metrics_df[self.metrics_df['ground_truth_location'] == vineyard].drop_duplicates()
            TP_dict[vineyard] = len(select_df[select_df['TP'] == True])
            FN_dict[vineyard] = len(select_df[select_df['F_'] == True])

        for vineyard in TP_dict.keys():
            recall = TP_dict[vineyard] / (TP_dict[vineyard] + FN_dict[vineyard])
            class_size = TP_dict[vineyard] + FN_dict[vineyard]
            weighted_recall_dict[vineyard] = (class_size * recall)
            total_dict[vineyard] = class_size

        weighted_avg_recall = np.sum(list(weighted_recall_dict.values()))/(np.sum(list(total_dict.values())))

        return weighted_avg_recall, weighted_recall_dict, total_dict

    def clustering_precision(self):
        TP_dict = dict()
        FP_dict = dict()
        precision_dict = dict()

        true_locs_list = self.metrics_df['predicted_location'].unique()

        for vineyard in true_locs_list:
            select_df = self.metrics_df[self.metrics_df['predicted_location'] == vineyard].drop_duplicates()
            TP_dict[vineyard] = len(select_df[select_df['TP'] == True])
            FP_dict[vineyard] = len(select_df[select_df['F_'] == True])

        for vineyard in TP_dict.keys():
            if str(vineyard) == "nan":  # not assigned a cluster, skip
                continue 
            precision = TP_dict[vineyard] / (TP_dict[vineyard] + FP_dict[vineyard])
            precision_dict[vineyard] = precision
            class_size = TP_dict[vineyard] + FP_dict[vineyard]

        avg_precision = np.mean(list(precision_dict.values()))

        return avg_precision, precision_dict

    def clustering_weighted_precision(self):
        TP_dict = dict()
        FP_dict = dict()
        weighted_precision_dict = dict()
        total_dict = dict()

        true_locs_list = self.metrics_df['predicted_location'].unique()

        for vineyard in true_locs_list:
            select_df = self.metrics_df[self.metrics_df['predicted_location'] == vineyard].drop_duplicates()
            TP_dict[vineyard] = len(select_df[select_df['TP'] == True])
            FP_dict[vineyard] = len(select_df[select_df['F_'] == True])

        for vineyard in TP_dict.keys():
            if str(vineyard) == "nan":  # not assigned a cluster, skip
                continue 
            precision = TP_dict[vineyard] / (TP_dict[vineyard] + FP_dict[vineyard])
            class_size = TP_dict[vineyard] + FP_dict[vineyard]
            weighted_precision_dict[vineyard] = (class_size * precision)
            total_dict[vineyard] = class_size

        weighted_avg_precision = np.sum(list(weighted_precision_dict.values()))/(np.sum(list(total_dict.values())))

        return weighted_avg_precision, weighted_precision_dict, total_dict

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()									# initialize the argParser
    
    argparser.add_argument(	"-c", "--clusterFile", 							
							help="CSV of clusters with predicted locations",
                            type=str,
							default=None,
							required=True)	


    flags = argparser.parse_args()

    metrics = ClusteringMetrics(flags.clusterFile
                                )
    print("\n\nRECALL: ")
    for recall in metrics.clustering_recall():
        print(recall)
    print("WEIGHTED RECALL: ")
    for w_recall in metrics.clustering_weighted_recall():
        print(w_recall)
    print("PRECISION: ")
    for precision in metrics.clustering_precision():
        print(precision)
    print("WEIGHTED PRECISION: ")
    for w_precision in metrics.clustering_weighted_precision():
        print(w_precision)
