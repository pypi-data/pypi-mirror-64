import pandas as pd
import logging as log
import collections
import re
import random


class df:
    df = pd.DataFrame(index=[""], columns=[""])

    def __init__(self, dataframe):
        self.df = dataframe.copy()

    def filter_regex(self, column_name, regex_strings):
        indices = []

        filters = regex_strings

        if not isinstance(regex_strings, list):
            filters = [regex_strings]

        for regex_string in filters:
            filtered_indices = list(self.df[self.df[column_name].apply(
                regex_filter, regex=regex_string)].index.values)
            if len(filtered_indices) > 0:
                indices = merge_array(indices, filtered_indices)

        return indices

    def filter_string(self, column_name, strings):
        indices = []

        filters = strings

        if not isinstance(strings, list):
            filters = [strings]

        for string in filters:
            filtered_indices = list(
                self.df[self.df[column_name] == string].index.values)
            if len(filtered_indices) > 0:
                indices = merge_array(indices, filtered_indices)

        return indices

    def filter_number(self, column_name, allowed_numbers):
        indices = []

        filters = allowed_numbers

        if not isinstance(allowed_numbers, list):
            filters = [allowed_numbers]

        for allowed_number in filters:
            filtered_indices = list(
                self.df[self.df[column_name] == float(allowed_number)].index.values)

            if len(filtered_indices) > 0:
                indices = merge_array(indices, filtered_indices)

        return indices

    def filter_type(self, column_name, allowed_types):
        indices = []
        types = ["string", "number", "int", "float"]

        filters = allowed_types

        if not isinstance(allowed_types, list):
            filters = [allowed_types]

        for allowed_type in filter:
            filtered_indices = []
            if allowed_type not in types:
                log.fatal("Invalid type: " + allowed_type)
                return

            if allowed_type == "number":
                filtered_indices = list(self.df[self.df[column_name].apply(
                    is_number)].index.values)

            if allowed_type == "int":
                filtered_indices = list(self.df[self.df[column_name].apply(
                    is_int)].index.values)

            if allowed_type == "float":
                filtered_indices = list(self.df[self.df[column_name].apply(
                    is_float)].index.values)

            if allowed_type == "string":
                filtered_indices = list(self.df[self.df[column_name].apply(
                    is_string)].index.values)

            if len(filtered_indices) > 0:
                indices = merge_array(indices, filtered_indices)

        return indices

    def filter_null(self, column_name):
        indices = self.df[self.df[column_name].isnull()].index.values

        return indices

    def remove_by_filter(self, indices):
        self.df = self.df[~self.df.index.isin(indices)]

        return len(indices)

    def remove_by_filter_inverted(self, indices):
        self.df = self.df[self.df.index.isin(indices)]

        return len(indices)

    def remove_by_column_name(self, column_name):
        self.df = self.df.drop(columns=column_name)

    def invert_indices(self, indices):
        return list(self.df[~self.df.index.isin(indices)].index.values)

    def replace_by(self, column_name, indices, value):
        self.df.loc[indices, column_name] = value

    def replace_by_mean(self, column_name, indices):
        mean = self.df[column_name].mean()
        self.df.loc[indices, column_name] = mean

    def replace_by_median(self, column_name, indices):
        median = self.df[column_name].median()
        self.df.loc[indices, column_name] = median

    def replace_by_random(self, column_name, indices, random_values):
        for index in indices:
            self.df.loc[index, column_name] = random.choice(random_values)

    def normalize_number_between(self, column_name, min, max):
        maxColumnValue = self.df[column_name].max()
        minColumnValue = self.df[column_name].min()

        a = (max-min)/(maxColumnValue-minColumnValue)
        b = min - (a * minColumnValue)

        self.df[column_name] = self.df[column_name].apply(
            lambda oldValue: a * oldValue + b)


# --- HELPERS ---


# Merge array without duplicates
def merge_array(one, two):
    return list(set().union(one, two))


def is_number(val):
    if is_float(val) or is_int(val):
        return True
    return False


def is_int(val):
    try:
        num = int(val)
    except ValueError:
        return False
    return True


def is_float(val):
    try:
        num = float(val)
    except ValueError:
        return False
    return True


def is_string(val):
    return not(is_number(val)) and val != ""


def regex_filter(val, regex):
    if val:
        mo = re.search(regex, str(val))
        if mo:
            return True
        else:
            return False
    else:
        return False
