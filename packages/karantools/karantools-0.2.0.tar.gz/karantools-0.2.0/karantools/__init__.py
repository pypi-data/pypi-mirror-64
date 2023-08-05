from __future__ import print_function    
from collections import defaultdict
import random
import numpy as np
from contextlib import contextmanager
import sys
import os
import pickle
import requests
import zipfile
import io
import multiprocessing
from time import time as systime
import functools

def average(arr):
    return float(sum(arr)) / len(arr)

def average_or_0(arr):
    if len(arr):
        return float(sum(arr)) / len(arr)
    else:
        return 0

class AverageStreamer(object):
    def __init__(self):
        self.count = 0
        self.total = 0.0

    def add(self, x):
        self.total += x
        self.count += 1

    def query(self):
        return self.total / self.count

class MaxStreamer(object):
    def __init__(self):
        self.max = float('-inf')
        self.added = False

    def add(self, x):
        if not self.added:
            self.added = True
        self.max = max(self.max, x)

    def query(self):
        if not self.added:
            raise RuntimeError('No values added to streamer.')
        return self.max

class MinStreamer(object):
    def __init__(self):
        self.min = float('inf')
        self.added = False

    def add(self, x):
        if not self.added:
            self.added = True
        self.min = min(self.min, x)

    def query(self):
        if not self.added:
            raise RuntimeError('No values added to streamer.')
        return self.min

class MaxScoreStreamer(object):
    def __init__(self, score_fn):
        self.max = float('-inf')
        self.max_x = None

        self.added = False
        self.score_fn = score_fn

    def add(self, x):
        if not self.added:
            self.added = True
        score = self.score_fn(x)

        if score > self.max:
            self.max = score
            self.max_x = x

    def query(self):
        if not self.added:
            raise RuntimeError('No values added to streamer.')
        return self.max_x

    def query_score(self):
        if not self.added:
            raise RuntimeError('No values added to streamer.')
        return self.max

######################################################################
#                              ASSERTS                               #
######################################################################

def assert_and_print(x, condition):
    print(x)
    if not condition:
        print_bold("Assert condition does not hold.")
        assert(condition)

def assert_eq(a, b):
    if a != b:
        print_bold("Assert failed because the following two are unequal:")
        print(a)
        print(b)
        raise AssertionError()

def assert_float_eq(a, b, epsilon=1e-5):
    if abs(a - b) > epsilon:
        print_bold("Assert failed because the following two are unequal:")
        print(a)
        print(b)
        raise AssertionError()

def assert_neq(a, b):
    if a == b:
        print_bold("Assert failed because the following two are equal:")
        print(a)
        print(b)
        raise AssertionError()

def assert_float_neq(a, b, epsilon=1e-5):
    if abs(a - b) <= epsilon:
        print_bold("Assert failed because the following two are approximately equal:")
        print(a)
        print(b)
        raise AssertionError()

######################################################################
#                               COLORS                               #
######################################################################

class colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    LIGHTBLUE = '\033[38;5;38m'
    BLUE = '\033[94m'
    MAGENTA = '\033[38;5;207m'
    INDIGO = '\033[38;5;105m'
    PINK = '\033[38;5;213m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    SEQUENCES_START_LOCS = {'BLUE': 20, 'RED': 160, 'GREEN': 76, 'INDIGO': 105, 'PINK': 213, 'LIGHTBLUE': 38, 'MAGENTA': 207, 'PURPLE': 93, 'CYAN': 33, 'DARKCYAN': 27, 'YELLOW': 226}

    @classmethod
    def normalize(cls, color):
        return color.upper().replace('_', '').replace(' ', '').replace('-', '')

    @classmethod
    def get(cls, color):
        return getattr(cls, color)

    @classmethod
    def get_seq(cls, color, length):
        def loc_to_coordinates(loc):
            loc -= 16
            red = loc // 36
            loc = loc % 36 
            green = loc // 6
            loc = loc % 6
            blue = loc
            return [red, green, blue]

        def coordinates_to_loc(coord):
            return 16 + coord[0] * 36 + coord[1] * 6 + coord[2]

        def perturb_coordinates(coord, perturb_hint=[None, None, None]):
            while True:
                original_coord = coord[:]
                if perturb_hint[0] is None or perturb_hint[1] is None or perturb_hint[2] is None or random.random() < .05:
                    perturb_direction = random.choice([0, 1, 2])
                    perturb_sign = random.choice([-1, 1])
                    perturb_hint = [0, 0, 0]
                else:
                    noised_directions = np.abs(np.array(perturb_hint) + 0.5 * np.random.randn(3))
                    direction_probabilities =  noised_directions / noised_directions.sum()
                    perturb_direction = np.random.choice([0, 1, 2], p=direction_probabilities)

                    sign_probabilities = [(perturb_hint[perturb_direction] + 6) / 12.0, 1 - (perturb_hint[perturb_direction] + 6) / 12.0]
                    perturb_sign = np.random.choice([-1, 1], p=sign_probabilities)
                perturb_hint[perturb_direction] += perturb_sign
                coord[perturb_direction] += perturb_sign
                coord[perturb_direction] = max(0, coord[perturb_direction])
                coord[perturb_direction] = min(5, coord[perturb_direction])

                if original_coord != coord:
                    return perturb_hint

                
        def get_color_at_loc(loc):
            return '\033[38;5;%dm' % loc

        start_loc = cls.SEQUENCES_START_LOCS[color]
        coord = loc_to_coordinates(start_loc)

        color_seq = []
        perturb_hint = [None, None, None]

        for i in range(length):
            loc = coordinates_to_loc(coord)
            color_seq.append(get_color_at_loc(loc))

            perturb_hint = perturb_coordinates(coord, perturb_hint=perturb_hint)

        return color_seq

######################################################################
#                            DOWNLOAD/IO                             #
######################################################################

def lazy_load(construct_fn, filename):
    try: 
        with open(filename, 'rb') as f:
            x = pickle.load(f)
    except IOError:
        x = construct_fn()
        with open(filename, 'wb') as f:
            pickle.dump(x, f)
    return x

def download_and_extract_zip(url):
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall()

def read_lines(filename, map_fn):
    mapped_lines = []
    with open(filename, 'r') as f:
        for line in f:
            mapped_lines.append(map_fn(line))
    return mapped_lines

def prompt_yes_or_no(prompt):
    if sys.version_info[0] >= 3:
        get_input = input
    else:
        get_input = raw_input
    reply = str(get_input(prompt + ' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return prompt_yes_or_no("Please enter")

######################################################################
#                           TIME/PROFILING                           #
######################################################################

class time(object):
    start_time = None
    description = None
    previous_times = []

    @classmethod
    def start(cls, description='Task'):
        cls.start_time = systime()
        cls.description = description

    @classmethod
    def end(cls, silent=False):
        if cls.start_time is None:
            raise RuntimeError('Start needs to be called before end.')

        previous_time = systime() - cls.start_time
        des = cls.description

        cls.start_time = None
        cls.description = None

        if not silent:
            print_header_block('%s completed in %f seconds.' % (des, previous_time))

        cls.previous_times.append((des, previous_time))

    @classmethod
    def print_times(cls):
        if not cls.previous_times:
            raise RuntimeError('Start and end need to be called.')
        print('')
        for i, (des, previous_time) in enumerate(cls.previous_times):
            print('%s completed in %f seconds.' % (des, previous_time))

class timer(object):
    def __init__(self, description='Task'):
        self.start_time = None
        self.des = description

    def __enter__(self):
        self.start_time = systime()

    def __exit__(self, type, value, traceback):
        previous_time = systime() - self.start_time
        print_header_block('%s completed in %f seconds.' % (self.des, previous_time))

######################################################################
#                              PRINTING                              #
######################################################################

def print_bold(string):
    print(colors.BOLD + string + colors.END)

def print_color(string, color='RED'):
    color_string = colors.get(colors.normalize(color))
    print(color_string + string + colors.END)

def print_color_gradient(string, color='RED'):
    color_seq = colors.get_seq(colors.normalize(color), len(string))
    print(''.join([color_seq[i] + ch + colors.END for i, ch in enumerate(string)]))

def print_color_rainbow(*args, **kwargs):
    print_color_gradient(*args, **kwargs)

def print_comment_header_block(header_string, length=70, adjust_length=True):
    if adjust_length:
        length = max(len(header_string) + 2, length)
    print('#' * length)
    left_spaces = (length - 2 - len(header_string)) // 2
    right_spaces = length - 2 - len(header_string) - left_spaces
    print('#' + ' ' * left_spaces + header_string + ' ' * right_spaces + '#')
    print('#' * length)

def print_header_block(header_string, length=80, adjust_length=True, color='BOLD'):
    if adjust_length:
        length = max(len(header_string) + 2, length)
    print('-' * length)
    left_spaces = (length - len(header_string)) // 2
    right_spaces = length - len(header_string) - left_spaces
    print_color(' ' * left_spaces + header_string + ' ' * right_spaces, color=color)
    print('-' * length)

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

######################################################################
#                             EXECUTION                              #
######################################################################

def run_command(command_str, ignore_error=False):
    print_color('-' * 80, color='green')
    print_color(command_str, color='green')
    print_color('-' * 80, color='green')
    exit_status = os.system(command_str)

    if not exit_status == 0:
        print_bold("\nError while running command.")
        if not ignore_error:
            if prompt_yes_or_no('Continue running?'):
                return exit_status
            else:
                exit(1)

    return exit_status

