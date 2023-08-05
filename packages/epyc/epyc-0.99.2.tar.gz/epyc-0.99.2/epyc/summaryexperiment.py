#
# Copyright (C) 2016--2018 Simon Dobson
# 
# This file is part of epyc, experiment management in Python.
#
# epyc is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# epyc is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with epyc. If not, see <http://www.gnu.org/licenses/gpl.html>.

from epyc import *
import numpy


class SummaryExperiment(ExperimentCombinator):
    """An experiment combinator that takes an underlying experiment and
    returns summary statistics for some of its results. This only really makes
    sense for experiments that return lists of results, such as those conducted
    using :class:`RepeatedExperiment`, but it works with any experiment.

    When run, a summary experiment summarises the experimental
    results, creating a new set of results that include the mean and
    variance for each result that the underyling experiments
    generated. (You can also select which results to summarise.) The
    raw results are discarded. The new results have the names of the
    raw results with suffices for mean, median, variance, and extrema.

    The summarisation obviously only works on result keys coming from the
    underlying experiments that are numeric. The default behaviour is to try to
    summarise all keys: you can restrict this by providing a list of keys to the
    constructor in the summarised_results keyword argument.

    The summary calculations only include those experimental runs that succeeded,
    that is that have their status set to True. Failed runs are ignored."""

    # Additional metadata
    UNDERLYING_RESULTS = 'repetitions'                         #: Metadata relement for the number of results that were obtained
    UNDERLYING_SUCCESSFUL_RESULTS = 'successful_repetitions'   #: Metadata elements for the number of results that were summarised
    UNDERLYING_EXCEPTIONS = 'underlying_exceptions'            #: Metadata elements for any exceptions raised

    # Prefix and suffix tags attached to summarised result and metadata values
    MEAN_SUFFIX = '_mean'              #: Suffix for the mean of the underlying values
    MEDIAN_SUFFIX = '_median'          #: Suffix for the median of the underlying values
    VARIANCE_SUFFIX = '_variance'      #: Suffix for the variance of the underlying values
    MIN_SUFFIX = '_min'                #: Suffix for the minimum of the underlying values
    MAX_SUFFIX = '_max'                #: Suffix for the maximum of the underlying values
    
    
    def __init__( self, ex, summarised_results = None ):
        """Create a summarised version of the given experiment. The given
        fields in the experimental results will be summarised, defaulting to all.
        If there are fields that can't be summarised (because they're not
        numbers), remove them here.

        :param ex: the underlying experiment
        :param summarised_results: list of result values to summarise (defaults to all)"""
        super(SummaryExperiment, self).__init__(ex)
        self._summarised_results = summarised_results

    def _mean( self, k ):
        """Return the tag associated with the mean of k."""
        return k + self.MEAN_SUFFIX

    def _median( self, k ):
        """Return the tag associated with the median of k."""
        return k + self.MEDIAN_SUFFIX

    def _variance( self, k ):
        """Return the tag associated with the variance of k."""
        return k + self.VARIANCE_SUFFIX
    
    def _min( self, k ):
        """Return the tag associated with the minimum of k."""
        return k + self.MIN_SUFFIX
    
    def _max( self, k ):
        """Return the tag associated with the maximum of k."""
        return k + self.MAX_SUFFIX
    
    def summarise( self, results ):
        """Generate a summary of results from a list of result dicts
        returned by running the underlying experiment. By default we generate
        mean, median, variance, and extrema for each value recorded.

        Override this method to create different or extra summary statistics.

        :param results: an array of result dicts
        :returns: a dict of summary statistics"""
        if len(results) == 0:
            return dict()
        else:
            summary = dict()

            # work out the fields to summarise
            allKeys = results[0][Experiment.RESULTS].keys()
            ks = self._summarised_results
            if ks is None:
                # if we don't restrict, summarise all keys
                ks = allKeys
            else:
                # protect against a key that's not present
                ks = [ k for k in ks if k in allKeys ]
                
            # add the summary statistics
            for k in ks:
                # compute summaries for all fields we're interested in
                vs = [ res[Experiment.RESULTS][k] for res in results ]
                summary[self._mean(k)]     = numpy.mean(vs)
                summary[self._median(k)]   = numpy.median(vs)
                summary[self._variance(k)] = numpy.var(vs)
                summary[self._min(k)]      = numpy.min(vs)
                summary[self._max(k)]      = numpy.max(vs)
                    
            return summary   

    def do( self, params ):
        """Perform the underlying experiment and summarise its results.
        Our results are the summary statistics extracted from the results of
        the instances of the underlying experiment that we performed.

        We drop from the calculations any experiments whose completion status
        was False, indicating an error. Our own completion status will be
        True unless we had an error summarising a field (usually caused by trying
        to summarise non-numeric data).

        We record the exceptions generated by any experiment we summarise under
        the metadata key :attr:`SummaryExperiment.UNDERLYING_EXCEPTIONS`

        :param params: the parameters to the underlying experiment
        :returns: the summary statistics of the underlying results"""

        # perform the underlying experiment
        rc = self.experiment().run()
        
        # extract the result dicts as a list
        results = rc[Experiment.RESULTS]
        if not isinstance(results, list):
            # force to list
            results = [ rc ]

        # extract only the successful runs
        sresults = [ res for res in results if res[Experiment.METADATA][Experiment.STATUS] ]
        exs = [ res[Experiment.METADATA][Experiment.EXCEPTION] for res in results if not res[Experiment.METADATA][Experiment.STATUS] ]
       
        # add extra values to our metadata record
        self._metadata[self.UNDERLYING_RESULTS]            = len(results)
        self._metadata[self.UNDERLYING_SUCCESSFUL_RESULTS] = len(sresults)
        self._metadata[self.UNDERLYING_EXCEPTIONS]         = exs

        # construct summary results
        return self.summarise(sresults)

