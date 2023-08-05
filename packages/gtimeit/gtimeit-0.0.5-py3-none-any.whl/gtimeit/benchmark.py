#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 * A benchmark for python functions
 * 
 * Description : Allows to run multiple python functions a certain amount
 * of times and to compare there respective execution times.
 * Display curves of all the execution times.
 * Prototype benchmarking for complexity tests up to one variable parameter
 *
 * Note : More examples available in benchmark_examples
 * 
 * Examples :
 *   Basic usage :
 * bm = Benchmark()
 * bm.add(fct1, param1, param2, ...)
 * bm.add(fct2, param1, param2, ...)
 * bm.add(fctn, param1, param2, ...)
 * bm.run(20, multiplicator=100)
 * 
 *   Quick usage :
 * bm = Benchmark([fct1, fct2], 300)
 * 
 * Author : Thibault Charmet
 * Creation date : 09/2018
"""

import sys
import os
import itertools
import operator
from time import time

import numpy as np
# import pandas as pd

import matplotlib
# While GTK isn't avail everywhere, we use TkAgg backend to generate png
if sys.platform != "win32" and os.getenv("DISPLAY") is None :
    matplotlib.use("Agg")
else :
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class Benchmark():
    """A benchmark for python functions.

    Basic usage :
    bm = Benchmark()
    bm.add(fct1, param1, param2, ...)
    bm.add(fct2, param1, param2, ...)
    bm.add(fctn, param1, param2, ...)
    bm.run(20, multiplicator=100)
    
    Quick usage :
    bm = Benchmark([fct1, fct2], 300)

    """

    def __init__(self, procedures=None, size=10, cache=0, multiplicator=1, run=True, disp=True, plot=True):
        """
            procedures (list) : functions to add to benchmark without parameters (default : None)
            run (bool) : auto run benchmark (only if procedures are given) (default : True)

            Following arguments are used only if auto run is activated
            disp (bool) : auto display results of the benchmark (default : True)
            plot (bool) : auto plot results of the benchmark (default : True)
            size (int) : number of tests to launch (default : 10)
            cache (int) : number of non saved tests to launch (default : 0)
            multiplicator (int) : number of times to exectute each function for each test (default : 1)
        """

        # contains tuples of a function and its arguments
        self.all_callable = dict()
        # summed execution times for each function (s)
        self.totalExecTime = dict()
        # list of execution times for each function (ms)
        self.listExecTime = dict()
        # result of each function
        # only have sense for deterministic functions
        # without random or side effects
        # IDEA : list all the results and detect non deterministic functions
        #        method get_results()
        self.results = dict()

        # managing fast way to call the benchmark
        if procedures :
            for procedure in procedures:
                self.add(procedure)
            if run :
                self.run(size, cache, multiplicator, disp, plot)


    def add(self, method, *args, **keyargs):
        """
            add a function to the benchmark

            method (function) : callable function to benchmark
                all the function must have different names
            *args : arguments of the function
            **keyargs : named arguments of the function
        """

        # IDEA : have a way to rename the function
        name = method.__name__
        self.all_callable[name] = (method, args, keyargs)
        self.totalExecTime[name] = 0
        self.listExecTime[name] = []


    def update_sizes(self, size, cache, multiplicator):
        """Update the size, cache and multiplicator attributes."""
        self.size = size
        self.cache = cache
        self.multiplicator = multiplicator


    def cache_run(self):
        """Run all the callable without recording datas."""
        for name, caller in self.all_callable.items():
            method, args, keyargs = caller
            for t in range(self.cache):
                result = method(*args, **keyargs)


    def execute(self, name, method, *args, **keyargs):
        """Execute a callable and record informations about it."""
        start = time()
        for p in range(self.multiplicator):
            # calling the method with all the given arguments
            result = method(*args, **keyargs)
        duration = time() - start
        self.totalExecTime[name] += duration
        self.listExecTime[name].append(ms(duration))
        self.results[name] = result


    def run(self, size=10, cache=0, multiplicator=1, disp=True, plot=True, reset=True):
        """
            Run the benchmark.

            disp (bool) : auto display results of the benchmark
            plot (bool) : auto plot results of the benchmark
            reset (bool) : define if we reset previously recorded datas
                set to false will allows you to run the benchmark little by little
            size (int) : number of tests to launch (default : 10)
            cache (int) : number of non saved tests to launch (default : 0)
                allows to ignore effects caused by previous executions
            multiplicator (int) : number of times to exectute each function for each test (default : 1)
                each callable will be called exactly (size+cache) * multiplicator times
        """

        if reset :
            self.reset()
        self.update_sizes(size, cache, multiplicator)
        self.cache_run()

        for t in range(self.size):
            for name, caller in self.all_callable.items():
                method, args, keyargs = caller
                self.execute(name, method, *args, **keyargs)
        if disp:
            self.disp()
        if plot:
            self.plot()


    def complexity_run(self, interval, pos=0, constructor=None, cache=0, multiplicator=1, disp=True, plot=True, reset=True):
        """
            Run the benchmark with a variable argument.

            This method is a prototype.
            Add a variable argument to the benchmark represented by an interval,
            a position and a constructor.
            Allows to display complexity curves of the functions.
            Up to one non named argument.

            interval (int list) : range of values taken by the argument
            pos (int) : position of the argument with others arguments (default : 0)
            constructor (function) : a function returning an argument from an integer 
                generally the argument is of the size of the integer

            plot (bool) : auto plot results of the benchmark
            disp (bool) : auto display results of the benchmark
                (only if auto run activated)
            reset (bool) : define if we reset previously recorded datas
                set to false will allows you to run the benchmark little by little
            size (int) : number of tests to launch (default : 10)
            cache (int) : number of non saved tests to launch (default : 0)
                allows to ignore effects caused by previous executions
            multiplicator (int) : number of times to exectute each function for each test (default : 1)
                each callable will be called exactly (size+cache) * multiplicator times
        """

        # IDEA : add variable argument directly from add method (independently for each callable) ?
        #        the sizes need to be se same if we want the plot to have sense
        #        Create a complexity benchmark class instead ?

        if reset :
            self.reset()
        size = len(interval)
        self.update_sizes(size, cache, multiplicator)
        self.cache_run()
        
        for i in interval:
            if constructor :
                # IDEA : maybe use iterables instead
                variable = constructor(i)
            else :
                variable = i
            for name, caller in self.all_callable.items():
                method, args, keyargs = caller
                # we replace the static argument by the dynamic one
                new_args = args[:pos] + (variable,) + args[pos+1:]
                self.execute(name, method, *new_args, **keyargs)
        if disp:
            self.disp(result=False)
        if plot:
            self.plot()


    def reset(self):
        """Reset all the recorded values about callables."""
        for name in self.all_callable.keys():
            self.totalExecTime[name] = 0
            self.listExecTime[name] = []


    def calc_stats(self):
        """Compute usefull stats from recorded values."""
        self.sortedExecTime = sorted(self.totalExecTime.items(), key=operator.itemgetter(1))
        self.min_time = self.totalExecTime[min(self.totalExecTime, key=self.totalExecTime.get)]


    def disp(self, result=True):
        """
            Display on terminal results of the benchmark.

            result (bool) : print the value returned by each function (default : True)
        """

        self.calc_stats()

        print("Number of global calls : {}".format(self.size))
        print("Multiplicator of these calls : {}".format(self.multiplicator))
        print("Total number of function calls : {}".format(self.size * self.multiplicator))

        for name, exec_time in self.sortedExecTime:
            print("    ----------------------------     ")
            print("Function : {}".format(name))

            if result and name in self.results:
                print("Result : {} ".format(self.results[name]))

            if exec_time > 0 :
                print("Total execution time :   {} s".format(exec_time))
                print("Average execution time : {} ms".format(ms(exec_time / self.size)))
                print("Average individual execution time : {} ns".format(ns(exec_time / self.multiplicator / self.size)))
                print("{}% of the fastest.".format(100 * exec_time / self.min_time))


    def plot(self, individual=True, average=True, legend=True):
        """
            Display curves of the benchmark results.

            individual (bool) : Define if we display curve of all execution times (default : True)
                set false when size it too big (>400)
            average (bool) : Define if we display the average curve of all execution times  (default : True)
            legend (bool) : Define if we display the legend (default : True)
        """

        self.calc_stats()
        # iterable with one rainbow color per curve
        # the slowest ones will in the red
        colors = iter(cm.rainbow(np.linspace(0, 1, len(self.totalExecTime))))
        fig = plt.figure()
        for name, exec_time in self.sortedExecTime:  
            color = next(colors)
            avg = ms(exec_time / self.size)
            if self.size == 1:
                plt.plot([0, 1], [avg, avg], '-', label=name, color=color)
                plt.xlabel("call")
            else:
                if individual:
                    label = "{0} ({1:.2f}% of the fastest)".format(name, 100 * exec_time / self.min_time)
                    plt.plot(range(1, self.size+1), self.listExecTime[name], '-', label=label, color=color)
                if average:
                    plt.plot([1, self.size], [avg, avg], '--', label="average time for "+name, color=color)
                plt.xlabel("calls")
            plt.ylabel("time (ms)")

        # plot the legend in a différent figure as it could be voluminous
        if legend :
            ax = plt.gca()
            figLegend = plt.figure(figsize=(5, 2))
            plt.figlegend(*ax.get_legend_handles_labels(), loc='upper left')
            # plt.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0.)
        plt.show()


    def plot_percent(self):
        """
            Display stacked area chart of relative execution times.
        """

        print("Not available for Python 2.7.3")
        # python-graph-gallery.com/255-percentage-stacked-area-chart/
        # data = pd.DataFrame(self.listExecTime, index=range(1, self.times+1))
        # We need to transform the data from raw data to percentage (fraction)
        # sumed = data.sum(axis=1)
        # print(sumed)
        # data_perc = data.divide(sumed, axis=0)
        # print(data_perc)
        
        # plt.stackplot(range(1, self.times+1),  data_perc["plusEgaleN"],  data_perc["plusPuisEgaleN"], labels=['plusEgaleN','plusPuisEgaleN'])
        # plt.legend(loc='upper left')
        # plt.margins(0,0)
        # plt.title('100 % stacked area chart')
        # plt.show()


def ms(x):
    """Convert seconds to milliseconds"""
    return 1000 * x


def ns(x):
    """Convert seconds to milliseconds"""
    return 1000000 * x



# ------------------------------ EXAMPLES ------------------------------


def plusEgale(i=1):
    i += 1
    return i

def plusPuisEgale(i=1):
    i = i + 1
    return i


if __name__ == "__main__":

    # running 200 tests 100000 times each
    bm = Benchmark()
    bm.add(plusEgale, 42)
    bm.add(plusPuisEgale, 42)
    bm.run(200, multiplicator=100000)

    # short version for procedures
    # bm = Benchmark([plusEgale, plusPuisEgale], 200, multiplicator=100000)
