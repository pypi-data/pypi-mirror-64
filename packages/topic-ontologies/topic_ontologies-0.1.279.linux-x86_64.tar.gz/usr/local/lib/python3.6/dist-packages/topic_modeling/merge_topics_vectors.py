import numpy as np
from topic_modeling.topics import *
import csv
import logging

def merge_topics(topic_model):
    path_topic_vectors_part1 = get_path_document_vectors('sample','strategic-intelligence-sub-topics-part1',topic_model)
    path_topic_vectors_part2 = get_path_document_vectors('sample','strategic-intelligence-sub-topics-part2',topic_model)
    vectors_df_part1 = pd.read_pickle(path_topic_vectors_part1)
    vectors_df_part2 = pd.read_pickle(path_topic_vectors_part2)
    vectors_df_part2['document-vector-2']=vectors_df_part2.apply(lambda row:row['document-vector'],axis=1)
    del vectors_df_part2['document-vector']
    merged_df = pd.merge(vectors_df_part1,vectors_df_part2,on='document-id')
    #merged_df['merged-document-vector']=merged_df.apply(row[''])

    #return document_ids,document_vectors
