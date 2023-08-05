#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import itertools

from time import time
from math import floor, log10

import matplotlib
# While GTK isn't avail everywhere, we use TkAgg backend to generate png
if sys.platform != "win32" and os.getenv("DISPLAY") is None :
    matplotlib.use("Agg")
else :
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class PerfTracker() :

    def __init__(self):
        self.creation_time = time()
        # tracked
        self.called = dict()
        self.totalExecTime = dict()
        # slow
        self.listsExecTime = dict()
        self.call_pseudo_history = dict()

    def add(self, keyword):
        self.called[keyword] = 0
        self.totalExecTime[keyword] = 0
        self.listsExecTime[keyword] = []
        self.call_pseudo_history[keyword] = {"time" : [], "call" : [], "duration" : []}

    def try_to_add(self, keyword):
        if keyword not in self.called:
            self.add(keyword)

    def _plotListsExecTimes(self):
        colors = iter(cm.rainbow(np.linspace(0, 1, len(self.called))))
        for name, timeList in self.listsExecTime.items():
            if self.called[name] > 1:
                plt.figure()
                plt.title(name)
                plt.xlabel("calls")
                plt.ylabel("time (ms)")
                color = next(colors)
                msAvgTime = ms(self.totalExecTime[name] / self.called[name])
                ms_times = map(ms, timeList)
                plt.plot(range(1, self.called[name]+1), ms_times, 'b-', label=name, color=color)
                plt.plot([1, self.called[name]], [msAvgTime, msAvgTime], '--', label="average time for "+name, color=color)


    def _plotCallPseudoHistory(self):
        plt.figure()
        plt.xlabel("time (ms)")
        plt.ylabel("calls")
        plt.title("Pseudo history of all the function calls")
        colors = iter(cm.rainbow(np.linspace(0, 1, len(self.called))))
        # ax = plt.gca()
        for name in self.called.keys():
            color = next(colors)
            x = list(map(ms, self.call_pseudo_history[name]["time"]))
            height = [1] * len(self.call_pseudo_history[name]["time"])
            width = list(map(ms, self.call_pseudo_history[name]["duration"]))
            plt.bar(x, height, width, label=name, color=color)
        # figLegend = plt.figure(figsize = (5, 2))
        # plt.figlegend(*ax.get_legend_handles_labels(), loc = 'upper left')
        plt.legend(bbox_to_anchor=(0, 1), loc=2, borderaxespad=0.)


    def _plotTimePie(self):
        plt.figure()
        colors = cm.rainbow(np.linspace(0, 1, len(self.called)))
        # ax = plt.gca()
        weighted_values = np.divide(list(self.totalExecTime.values()), sum(self.totalExecTime.values()))
        plt.pie(weighted_values, labels=self.totalExecTime.keys(), colors=colors)
        plt.figtext(.65, .05, "Script execution time : {0:.4f}s".format(self.stop_time - self.creation_time))



    def disp_all(self):
        self.stop_time = time()
        for name in self.called.keys() :
            self.disp(name)
        # if there is something to display
        if self.called.keys():
            # self._plotListsExecTimes()
            self._plotCallPseudoHistory()
            self._plotTimePie()
            plt.show()

    def disp(self, name):
        print(" -- {} -- ".format(name))
        print("Number of calls : {}".format(self.called[name]))

        if self.called[name] > 0 :
            print("Total execution time :   {} s".format(self.totalExecTime[name]))

            if self.totalExecTime[name] > 0 :
                avgExecTime = self.totalExecTime[name] / self.called[name]
                print("Average execution time : {} ms".format(ms(avgExecTime)))



def ms(x):
    return 1000 * x


def significative_round(x):
    """Round a number to the first significative number"""
    return round(x, -int(floor(log10(abs(x)))))


def timeit(method):
    def timed(*args, **keyargs):
        start = time()
        result = method(*args, **keyargs)
        duration = (time() - start) * 1000
        if "log_time" in keyargs:
            name = keyargs.get("log_name", method.__name__.upper())
            keyargs["log_time"][name] = int(duration)
        else:
            print("%r  %2.2f ms" % (method.__name__, duration))
        return result
    return timed



def remove_time(duration):
    """Remove a time from all non finished functions"""
    for parent, history in PERF_TRACKER.call_pseudo_history.items():
        # all the non finished functions have a negative duration
        # each sub function remove this own execution time from
        # the parent function so we only keep the real time
        # used by the function
        if history["duration"][-1] <= 0 :
            history["duration"][-1] -= duration
            # print("substracting to "+parent)
            # print(PERF_TRACKER.call_pseudo_history[parent]["duration"][-1])

def remove_fictive_time(name):
    """Remove all the execution times of a given function of the parents functions
    Measuring the real execution time instead of a simple difference between start and end"""
    remove_time(PERF_TRACKER.call_pseudo_history[name]["duration"][-1])


# def stop_all(stop_time):
#     for name, history in PERF_TRACKER.call_pseudo_history.items():
#         if history["duration"][-1] <= 0 :
#             PERF_TRACKER.call_pseudo_history[name]["duration"][-1] += duration
#             PERF_TRACKER.totalExecTime[name] += duration



def execTimeList(method):
    def timed(*args, **keyargs):
        name = method.__name__
        PERF_TRACKER.try_to_add(name)
        PERF_TRACKER.called[name] += 1
        start = time()
        PERF_TRACKER.call_pseudo_history[name]["time"].append(start)
        PERF_TRACKER.call_pseudo_history[name]["duration"].append(0)
        result = method(*args, **keyargs)
        end = time()
        duration = end - start
        PERF_TRACKER.call_pseudo_history[name]["duration"][-1] += duration
        PERF_TRACKER.totalExecTime[name] += PERF_TRACKER.call_pseudo_history[name]["duration"][-1]
        PERF_TRACKER.listsExecTime[name].append(PERF_TRACKER.call_pseudo_history[name]["duration"][-1])
        # print("duration of "+name)
        # print(PERF_TRACKER.call_pseudo_history[name]["duration"][-1])
        remove_fictive_time(name)
        return result
    return timed


def display_performances():
    """ """
    start = time()
    PERF_TRACKER.disp_all()
    end = time()
    duration = start - start
    remove_time(duration)
    # stop_all()


PERF_TRACKER = PerfTracker()



# def execTime(method):
#     def timed(*args, **keyargs):
#     return timed


# def callCount(method):
#     def counted(*args, **keyargs):
#     return counted



def multicall(times):
    def real_multicall(method):
        def multicalled(*args, **keyargs):
            for x in range(times):
                result = method(*args, **keyargs)
            return result
        return multicalled
    return real_multicall


@execTimeList
def additions():
    i = 0
    for x in range(1,100000):
        i += 1

@execTimeList
def sumrange():
    sum(range(1,100000))

@execTimeList
def extending():
    l = []
    for x in range(1,100000):
        l.extend([0])

@execTimeList
def fct1():
    extending()
    sumrange()




# TODO pie plot of summed times
if __name__ == "__main__":

    # simulate some basic code
    for x in range(4):
        additions()
        sumrange()
        extending()
    for x in range(2):
        sumrange()
        extending()
    for x in range(10):
        additions()
    fct1()

    display_performances()