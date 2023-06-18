class ClusteringMetrics:
    def __init__(self, object_assignment_filename):
        self.metrics_df = pd.read_csv(object_assignment_filename)[['true_location','predicted_location_dbscan']].copy()
        self.metrics_df.loc[:,'TP'] = self.metrics_df.apply(lambda row : Levenshtein.ratio(row['true_location'], row['predicted_location_dbscan']) >= 0.7 , axis=1)
        self.metrics_df.loc[:,'F_'] = self.metrics_df.apply(lambda row : Levenshtein.ratio(row['true_location'], row['predicted_location_dbscan']) < 0.7 , axis=1)

    def clustering_recall(self):
        TP_dict = dict()
        FN_dict = dict()
        recall_dict = dict()

        true_locs_list = ['Alis_Vineyard', 'Little_River_Winery', 'Faber_Vineyard', 'Ugly_Duckling_Wines', 'Oakover_Grounds', 'Lancaster_Wines']

        for vineyard in true_locs_list:
            select_df = self.metrics_df[self.metrics_df['true_location'] == vineyard]
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

        true_locs_list = ['Alis_Vineyard', 'Little_River_Winery', 'Faber_Vineyard', 'Ugly_Duckling_Wines', 'Oakover_Grounds', 'Lancaster_Wines']

        for vineyard in true_locs_list:
            select_df = self.metrics_df[self.metrics_df['true_location'] == vineyard]
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

        true_locs_list = self.metrics_df['predicted_location_dbscan'].unique()

        for vineyard in true_locs_list:
            select_df = self.metrics_df[self.metrics_df['predicted_location_dbscan'] == vineyard]
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

        true_locs_list = self.metrics_df['predicted_location_dbscan'].unique()

        for vineyard in true_locs_list:
            select_df = self.metrics_df[self.metrics_df['predicted_location_dbscan'] == vineyard]
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
    metrics = ClusteringMetrics(directory_name+'/data/nic_output/ownershipAssignment/obj_df.csv')
    print("RECALL: ", metrics.clustering_recall())
    print("WEIGHTED RECALL: ", metrics.clustering_weighted_recall())
    print("PRECISION: ", metrics.clustering_precision())
    print("WEIGHTED PRECISION: ", metrics.clustering_weighted_precision())
