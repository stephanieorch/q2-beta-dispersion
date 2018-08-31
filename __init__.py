# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os.path
import collections
import urllib.parse
import pkg_resources
import itertools

import skbio
import skbio.diversity
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.sandbox.stats.multicomp import multipletests
import qiime2
import q2templates
from natsort import natsorted


TEMPLATES = pkg_resources.resource_filename('q2_diversity', '_beta')


def bioenv(output_dir: str, distance_matrix: skbio.DistanceMatrix,
           metadata: qiime2.Metadata) -> None:
    # Filter metadata to only include IDs present in the distance matrix.
    # Also ensures every distance matrix ID is present in the metadata.
    metadata = metadata.filter_ids(distance_matrix.ids)

    # drop non-numeric columns and empty columns
    pre_filtered_cols = set(metadata.columns)
    metadata = metadata.filter_columns(column_type='numeric')
    non_numeric_cols = pre_filtered_cols - set(metadata.columns)

    # filter 0 variance numerical columns and empty columns
    pre_filtered_cols = set(metadata.columns)
    metadata = metadata.filter_columns(drop_zero_variance=True,
                                       drop_all_missing=True)
    zero_variance_cols = pre_filtered_cols - set(metadata.columns)

    # Drop samples that have any missing values.
    # TODO use Metadata API if this type of filtering is supported in the
    # future.
    df = metadata.to_dataframe()
    df = df.dropna(axis='index', how='any')

    # filter the distance matrix to exclude samples that were dropped from
    # the metadata, and keep track of how many samples survived the filtering
    # so that information can be presented to the user.
    initial_dm_length = distance_matrix.shape[0]
    distance_matrix = distance_matrix.filter(df.index)
    filtered_dm_length = distance_matrix.shape[0]

    result = skbio.stats.distance.bioenv(distance_matrix, df)
    result = q2templates.df_to_html(result)

    index = os.path.join(TEMPLATES, 'bioenv_assets', 'index.html')
    q2templates.render(index, output_dir, context={
        'initial_dm_length': initial_dm_length,
        'filtered_dm_length': filtered_dm_length,
        'non_numeric_cols': ', '.join(sorted(non_numeric_cols)),
        'zero_variance_cols': ', '.join(sorted(zero_variance_cols)),
        'result': result})


_beta_group_significance_fns = {'permanova': skbio.stats.distance.permanova,
                                'anosim': skbio.stats.distance.anosim,
                                'permdisp': skbio.stats.distance.permdisp}
