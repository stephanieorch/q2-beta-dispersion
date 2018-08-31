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
from q2_types.distance_matrix import DistanceMatrix
from q2_types.sample_data import SampleData
from q2_sample_classifier.plugin_setup import (
    parameters, parameter_descriptions, output_descriptions,
    pipeline_parameters, pipeline_parameter_descriptions,
    regressor_pipeline_outputs, pipeline_output_descriptions, regressors)


miscellaneous_parameter_descriptions = {
    'state_column': ('Metadata column containing state (time) variable '
                     'information.'),
    'replicate_handling': (
        'Choose how replicate samples are handled. If replicates are '
        'detected, "error" causes method to fail; "drop" will discard all '
        'replicated samples; "random" chooses one representative at random '
        'from among replicates.')
}



plugin.methods.register_function(
    function=beta_dispersion,
    inputs={'distance_matrix': DistanceMatrix},
    parameters={ 'metadata': Metadata,
                 'palette': Str % Choices([
                      'Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Paired', 'Accent',
                      'Dark2', 'tab10', 'tab20', 'tab20b', 'tab20c', 'viridis', 'plasma',
                      'inferno', 'magma', 'terrain', 'rainbow']),
                'metric': Str,
                'group_column': Str,
                'replicate_handling': miscellaneous_parameters['replicate_handling']
                'state_column': miscellaneous_parameters['state_column'],
    outputs=[('beta_volaility', SampleData[FirstDifferences])], #UNKNOWN WHAT TO PUT INSTEAD OF SAMPLEDATA
    input_descriptions={
        'distance_matrix': 'Matrix of distances between pairs of samples.'},
    parameter_descriptions={
        'metadata': ('Metadata'),
        'palette': Str % Choices([
            'Set1', 'Set2', 'Set3', 'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'tab10', 'tab20', 'tab20b', 'tab20c', 'viridis', 'plasma',
            'inferno', 'magma', 'terrain', 'rainbow']
        'metric': ('The beta diversity metric used to compute the beta distance matrix.'
        'group_column': (
            'Metadata column on which to separate groups for comparison'),
        'replicate_handling': (
            miscellaneous_parameter_descriptions['replicate_handling']),
        'state_column': ('Metadata column containing state (e.g., Time) '
                         'across which samples are paired.'),
}
                   
    output_descriptions={'beta_dispersion': 'The resulting beta dispersion graph.'},
    name=('Calculates average beta distance and standard deviation between groups in a metadata column.'),
    description=(
        'Calculates average beta diversity distance between separate groups '
        'at two or more states.'
        'Outputs a line plot of the average values and their error bars'
        'for each comparison of two groups in a category at each '
        'sequential pair of states.'
)
