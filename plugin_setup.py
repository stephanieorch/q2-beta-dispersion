# ----------------------------------------------------------------------------
# Copyright (c) 2017-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import importlib

from qiime2.plugin import (Str, Bool, Plugin, Metadata, Choices, Range, Float,
                           Citations, Visualization)
from q2_types.feature_table import FeatureTable, RelativeFrequency, Frequency
from q2_types.distance_matrix import DistanceMatrix
from q2_types.sample_data import SampleData
from q2_types.feature_data import FeatureData

from q2_sample_classifier import (Importance, RegressorPredictions,
                                  SampleEstimator, Regressor)
from q2_sample_classifier.plugin_setup import (
    parameters, parameter_descriptions, output_descriptions,
    pipeline_parameters, pipeline_parameter_descriptions,
    regressor_pipeline_outputs, pipeline_output_descriptions, regressors)


from ._type import FirstDifferences
from ._format import FirstDifferencesFormat, FirstDifferencesDirectoryFormat
from ._longitudinal import (pairwise_differences, pairwise_distances,
                            linear_mixed_effects, volatility, nmit,
                            first_differences, first_distances,
                            maturity_index, feature_volatility,
                            plot_feature_volatility)
import q2_longitudinal


citations = Citations.load('citations.bib', package='q2_longitudinal')

plugin = Plugin(
    name='longitudinal',
    version=q2_longitudinal.__version__,
    website="https://github.com/qiime2/q2-longitudinal",
    package='q2_longitudinal',
    description=(
        'This QIIME 2 plugin supports methods for analysis of time series '
        'data, involving either paired sample comparisons or longitudinal '
        'study designs.'),
    short_description='Plugin for paired sample and time series analyses.',
    citations=[citations['bokulich2017q2']]
)

plugin.register_semantic_types(FirstDifferences)

plugin.register_formats(
    FirstDifferencesFormat, FirstDifferencesDirectoryFormat)

plugin.register_semantic_type_to_format(
    SampleData[FirstDifferences],
    artifact_format=FirstDifferencesDirectoryFormat)

miscellaneous_parameters = {
    'state_column': Str,
    'replicate_handling': Str % Choices(['error', 'random', 'drop'])
}

shared_parameters = {
    'metadata': Metadata,
    'individual_id_column': Str,
}

base_parameters = {
    **shared_parameters,
    'state_column': miscellaneous_parameters['state_column'],
    'palette': Str % Choices([
        'Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Paired', 'Accent',
        'Dark2', 'tab10', 'tab20', 'tab20b', 'tab20c', 'viridis', 'plasma',
        'inferno', 'magma', 'terrain', 'rainbow']),
}

paired_params = {
    **base_parameters,
    'group_column': Str,
    'state_1': Str,
    'state_2': Str,
    'parametric': Bool,
    'replicate_handling': miscellaneous_parameters['replicate_handling'],
}

miscellaneous_parameter_descriptions = {
    'state_column': ('Metadata column containing state (time) variable '
                     'information.'),
    'replicate_handling': (
        'Choose how replicate samples are handled. If replicates are '
        'detected, "error" causes method to fail; "drop" will discard all '
        'replicated samples; "random" chooses one representative at random '
        'from among replicates.')
}

shared_parameter_descriptions = {
        'metadata': (
            'Sample metadata file containing individual_id_column.'),
        'individual_id_column': (
            'Metadata column containing IDs for individual subjects.'),
}

base_parameter_descriptions = {
        **shared_parameter_descriptions,
        'palette': 'Color palette to use for generating boxplots.',
}

paired_parameter_descriptions = {
        **base_parameter_descriptions,
        'group_column': (
            'Metadata column on which to separate groups for comparison'),
        'individual_id_column': (
            'Metadata column containing subject IDs to use for pairing '
            'samples. WARNING: if replicates exist for an individual ID at '
            'either state_1 or state_2, that subject will be dropped and '
            'reported in standard output by default. Set '
            'replicate_handling="random" to instead randomly select one '
            'member.'),
        'state_column': ('Metadata column containing state (e.g., Time) '
                         'across which samples are paired.'),
        'state_1': 'Baseline state column value.',
        'state_2': 'State column value to pair with baseline.',
        'parametric': ('Perform parametric (ANOVA and t-tests) or non-'
                       'parametric (Kruskal-Wallis, Wilcoxon, and Mann-'
                       'Whitney U tests) statistical tests.'),
        'replicate_handling': (
            miscellaneous_parameter_descriptions['replicate_handling']),
}

