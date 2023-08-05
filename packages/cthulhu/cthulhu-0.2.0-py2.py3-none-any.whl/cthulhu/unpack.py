# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# Python 2 and 3 compatibility
from __future__ import print_function, division

import sys
import pickle
import json

import numpy as np
from cthulhu.rts_log_tools import rts2dict


def unpack_data(data_file, verbosity=0):
    if isinstance(data_file, str):
        # Pickle
        if data_file.endswith(".pickle"):
            with open(data_file, 'r') as f:
                # If an exception is raised about encoding, try loading without it.
                try:
                    unpacked = pickle.load(f, encoding="UTF-8")
                except TypeError:
                    unpacked = pickle.load(f)
            if verbosity > 0:
                print("Loaded pickle file: %s" % data_file)
            return unpacked

        # JSON
        elif data_file.endswith(".json"):
            with open(data_file, 'r') as f:
                unpacked = json.load(f)
            if verbosity > 0:
                print("Loaded JSON file: %s" % data_file)
            return unpacked

        # YAML
        elif data_file.endswith(".yaml"):
            # Import YAML here so that if you don't have YAML installed, but
            # you're not using YAMLs, you won't be bothered about it!
            import yaml
            try:
                from yaml import CSafeLoader as SafeLoader
            except ImportError:
                from yaml import SafeLoader
                print("LibYAML not available - using pure Python implementation (slower).", file=sys.stderr)

            with open(data_file, 'r') as f:
                unpacked = yaml.load(f, Loader=SafeLoader)
            if verbosity > 0:
                print("Loaded YAML file: %s" % data_file)
            return unpacked

        # Will perform the scraping on a specified log file.
        # N.B. This is computationally expensive, and other
        # tools should be used to convert RTS logs into an
        # intermediate format, especially if the data is to
        # be used more than once.
        elif data_file.endswith(".log"):
            reduced = rts2dict(data_file)
            if verbosity > 0:
                print("Loaded RTS log file: %s" % data_file)
            return reduced

        # Text file - can only be in a numpy.loadtxt format with
        # the four required lists.
        elif data_file.endswith(".txt"):
            ra, dec, ra_shifts, dec_shifts = np.loadtxt(data_file)
            if verbosity > 0:
                print("Loaded text file: %s" % data_file)
            return [ra, dec, ra_shifts, dec_shifts]

        else:
            raise ValueError("cthulhu does not recognise your file ({})!".format(data_file))

    elif isinstance(data_file, list):
        # If data_file is a list, assume it's a list of lists structured:
        # ["ra", "dec", "ra_shifts", "dec_shifts"]
        return data_file
