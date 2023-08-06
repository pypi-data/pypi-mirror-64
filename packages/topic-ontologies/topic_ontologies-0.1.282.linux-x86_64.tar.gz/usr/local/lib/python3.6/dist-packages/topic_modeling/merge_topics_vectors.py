import numpy as np
from conf.configuration import *
import pandas as pd
import csv
import logging
logging

def merge_topics(topic_model):
    path_topic_vectors_part1 = get_path_document_vectors('sample','strategic-intelligence-sub-topics-part1',topic_model)
    path_topic_vectors_part2 = get_path_document_vectors('sample','strategic-intelligence-sub-topics-part2',topic_model)
    path_final_merged_document_vectors=get_path_document_vectors('sample','strategic-intelligence-sub-topics',topic_model)
    logging.warning("part 1 path %s"%path_topic_vectors_part1)
    logging.warning("part 2 path %s"%path_topic_vectors_part2)

    vectors_df_part1 = pd.read_pickle(path_topic_vectors_part1)
    vectors_df_part2 = pd.read_pickle(path_topic_vectors_part2)

    logging.warning("part 1 shape %s"%str(vectors_df_part1.shape))
    logging.warning("part 1 dimension %s"%str(vectors_df_part1['document-vector'].shape))
    logging.warning("part 2 shape %s"%str(vectors_df_part2.shape))
    vectors_df_part1.rename(columns={'document-vector':'document-vector-2'},inplace=True)


    del vectors_df_part2['document-vector']
    logging.warning("final columns of part 2 df %s"%vectors_df_part2.info())
    logging.warning("final columns of part 1 df %s"%vectors_df_part1.info())

    merged_df = pd.merge(vectors_df_part1,vectors_df_part2,on='document-id')
    merged_df['merged-document-vector']=merged_df.apply(lambda row:np.concatenate([row['document-vector'],row['document-vector-2']]),axis=1)
    del merged_df['document-vector']
    logging.warning("final columns final dataset df %s"%vectors_df_part1.info())

    merged_df.rename(columns={'document-vector':'merged-document-vector'},inplace=True)
    logging.warning("final columns final dataset df %s"%merged_df.info())
    logging.warning("final shape final dataset df %s"%str(merged_df.shape))
    logging.warning("final path %s"%str(path_final_merged_document_vectors))
    merged_df.to_pickle(path_final_merged_document_vectors)
    #return document_ids,document_vectors

merge_topics('word2vec-esa-100')