#!python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

# An all-in-one script for running cthulhu over data. Its main purpose is to
# print ionospheric statistics for input data, but it can generate plots too.

# Python 2 and 3 compatibility
from __future__ import print_function, division

import os
import sys
import glob
import argparse
import multiprocessing as mp

import numpy as np

from cthulhu.reconstruct import Obsid
from cthulhu.unpack import unpack_data
from cthulhu.plot_tools import generate_diagnostic_figure, raw_and_tec
from pyGrad2Surf.g2s import g2s, g2s_spectral, g2s_dirichlet, g2s_weighted

# Import tqdm without enforcing it as a dependency
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(*args, **kwargs):
        if args:
            return args[0]
        return kwargs.get("iterable", None)


def print_around_progress(text, file=sys.stdout):
    if args.progress:
        print("")
    print(text, file=file)


def unpack_model_plot(data_file):
    if args.verbosity > 2:
        print("Attempting to unpack: %s" % data_file)

    unpacked = unpack_data(data_file, verbosity=args.verbosity)
    # Check if there's any data in the file; otherwise exit.
    if unpacked is None:
        print("unpack_data returned None for %s" % data_file, file=sys.stderr)
        return None

    if len(unpacked["sources"]) == 0:
        print_around_progress("%s: No data contained." % data_file, file=sys.stderr)
        return None

    if args.field:
        mean_ra = np.mean([unpacked["sources"][s]["ra"] for s in unpacked["sources"]])
        mean_dec = np.mean([unpacked["sources"][s]["dec"] for s in unpacked["sources"]])

        if args.field.lower() == "eor0":
            if abs(mean_ra + 0) > args.field_tol or abs(mean_dec + 27) > args.field_tol:
                print_around_progress("%s: Not EoR0, skipping." % data_file, file=sys.stderr)
                return None
        if args.field.lower() == "eor1":
            if abs(mean_ra - 60) > args.field_tol or abs(mean_dec + 27) > args.field_tol:
                print_around_progress("%s: Not EoR1, skipping." % data_file, file=sys.stderr)
                return None

    if args.directional_cosines:
        x_pos = "l"
        y_pos = "m"
        x_shift = "l_shifts"
        y_shift = "m_shifts"
    else:
        x_pos = "ra"
        y_pos = "dec"
        x_shift = "ra_shifts"
        y_shift = "dec_shifts"
    # Average all data, excepting the amount to be flagged.
    if not args.high_res:
        x, y, x_shifts, y_shifts = [], [], [], []
        sources, flux_densities = [], []
        for s in unpacked["sources"]:
            if int(unpacked["sources"][s]["source_number"]) > args.number_of_sources:
                break

            x.append(unpacked["sources"][s][x_pos])
            y.append(unpacked["sources"][s][y_pos])

            if args.flag_end == 0:
                x_shifts.append(np.nanmean(unpacked["sources"][s][x_shift][args.flag_front:]))
                y_shifts.append(np.nanmean(unpacked["sources"][s][y_shift][args.flag_front:]))
            else:
                x_shifts.append(np.nanmean(unpacked["sources"][s][x_shift][args.flag_front:-args.flag_end]))
                y_shifts.append(np.nanmean(unpacked["sources"][s][y_shift][args.flag_front:-args.flag_end]))
            sources.append(s)
            flux_densities.append(unpacked["sources"][s]["flux_density"])

        obs = Obsid((x, y,
                     np.array(x_shifts),
                     np.array(y_shifts)),
                    obsid=unpacked["metadata"]["obsid"],
                    sources=sources,
                    flux_densities=flux_densities,
                    radius=args.radius)
        obs.pca()
        obs.obsid_metric()

        if args.plots:
            obs.reconstruct_tec(g2s_method=g2s_method)
            obs.tec_power_spectrum()
            obs.save_tec_fits(comment="Average of %s %ss intervals" %
                              (unpacked["metadata"]["iterations"]-args.flag_front-args.flag_end,
                               unpacked["metadata"]["cadence"]),
                              verbosity=args.verbosity, overwrite=overwrite)
            generate_diagnostic_figure(obs, verbosity=args.verbosity, overwrite=overwrite)
            raw_and_tec(obs, verbosity=args.verbosity, overwrite=overwrite,
                        title="Obsid: %s (Average of %s %ss intervals)\nMetric: %.4f PCA eigenvalue: %.4f" %
                        (obs.obsid, unpacked["metadata"]["iterations"]-args.flag_front-args.flag_end,
                         unpacked["metadata"]["cadence"], obs.metric, obs.pca_variance[0]))

        string = str(obs.obsid)
        for x in obs.metrics:
            string += " %.4f" % x[0]
        string += " %.4f" % obs.metric
        return string

    # For each epoch (timestamp) in the data, bundle the ionospheric shifts and pass them
    # to cthulhu.
    else:
        results = []
        for i, t in enumerate(unpacked["metadata"]["timestamps"]):
            if i < args.flag_front or i + args.flag_end > len(unpacked["metadata"]["timestamps"]) - 1:
                continue

            x, y, x_shifts, y_shifts = [], [], [], []
            sources, flux_densities = [], []
            for s in unpacked["sources"]:
                if int(unpacked["sources"][s]["source_number"]) > args.number_of_sources:
                    break

                x_s = unpacked["sources"][s][x_shift][i]
                y_s = unpacked["sources"][s][y_shift][i]
                if np.isfinite(x_s):
                    x.append(unpacked["sources"][s][x_pos])
                    y.append(unpacked["sources"][s][y_pos])
                    x_shifts.append(x_s)
                    y_shifts.append(y_s)
                    sources.append(s)
                    flux_densities.append(unpacked["sources"][s]["flux_density"])

            if len(x) < 500:
                print_around_progress("%s: Too few sources, skipping." % t, file=sys.stderr)
                continue

            obs = Obsid((x, y,
                         np.array(x_shifts),
                         np.array(y_shifts)),
                        obsid=t, sources=sources,
                        flux_densities=flux_densities,
                        radius=args.radius)
            obs.pca()
            obs.obsid_metric()

            if args.plots or args.fits:
                obs.reconstruct_tec(g2s_method=g2s_method)

                if args.plots:
                    obs.tec_power_spectrum()
                    generate_diagnostic_figure(obs, verbosity=args.verbosity, overwrite=overwrite,
                                               filename="%s.png" % t, directory="plots_8s")
                    raw_and_tec(obs, verbosity=args.verbosity, overwrite=overwrite,
                                filename="%s.png" % t, directory="raw_and_tec_8s",
                                title="Obsid: %s + %ss (%ss cadence)\nMetric: %.4f PCA eigenvalue: %.4f" % (obs.obsid, t - obs.obsid,
                                                                                                            unpacked["metadata"]["cadence"],
                                                                                                            obs.metric, obs.pca_variance[0]))

                if args.fits:
                    # To ensure that the dimensions of the an output fits file are exactly the same,
                    # overwrite the tec_extent with something consistent.
                    try:
                        obs.tec_extent = tec_extent
                    except NameError:
                        tec_extent = obs.tec_extent
                    obs.save_tec_fits(comment="%ss interval snapshot" % unpacked["metadata"]["cadence"],
                                      filename="%s.fits" % t, directory="fits_files_8s",
                                      verbosity=args.verbosity, overwrite=overwrite)

            string = str(t)
            for x in obs.metrics:
                string += " %.4f" % x[0]
            string += " %.4f" % obs.metric
            results.append(string)
        return "\n".join(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity", action="count", default=0,
                        help="Level of verbosity.")
    parser.add_argument("--no_overwrite", action="store_true",
                        help="Don't overwrite existing plots and files.")
    parser.add_argument("-d", "--directional_cosines", action="store_true",
                        help="Use (l,m) coordinates for calculations.")
    parser.add_argument("-n", "--number_of_sources", default=np.inf, type=int,
                        help="Include only the first n sources.")
    parser.add_argument("--high_res", action="store_true",
                        help="Use each epoch of the data, rather than an average of the data. Default: %(default)s")
    parser.add_argument("--flag_front", default=1, type=int,
                        help="Flag this many epochs at the front of each file. Default: %(default)s")
    parser.add_argument("--flag_end", default=1, type=int,
                        help="Flag this many epochs at the end of each file. Default: %(default)s")
    parser.add_argument("-r", "--radius", type=float,
                        help="Specify the radius to include sources.")
    parser.add_argument("-p", "--plots", action="store_true",
                        help="Produce plots from the data. Default: %(default)s")
    parser.add_argument("-f", "--fits", action="store_true",
                        help="Produce fits files from the data. Default: %(default)s")
    parser.add_argument("--field", type=str,
                        help="Only accept data from the field specified. "
                        "Currently only works for 'EoR0' or 'EoR1'. By default, no data is rejected.")
    parser.add_argument("--field_tol", default=10, type=float,
                        help="Tolerance on the location of the specified field. Default: %(default)s")
    parser.add_argument("--g2s_method", default="g2s",
                        help="Method to use for TEC reconstruction. Default: %(default)s")
    parser.add_argument("--processes", default=mp.cpu_count(), type=int,
                        help="The number of processes in parallel. Default: %(default)s.")
    parser.add_argument("--progress", action="store_true",
                        help="Display a progress bar. Default: %(default)s.")
    parser.add_argument("files", nargs='*', help="Files to be processed. "
                        "See cthulhu.unpack_data for appropriate formats.")
    args = parser.parse_args()

    # Check that field arguments are sane.
    if args.field and args.field.lower() not in ["eor0", "eor1"]:
        print("Unknown field specified (%s)." % args.field, file=sys.stderr)
        exit(1)

    if args.g2s_method.lower() == "g2s":
        g2s_method = g2s
    elif args.g2s_method.lower() == "g2s_spectral":
        g2s_method = g2s_spectral
    elif args.g2s_method.lower() == "g2s_dirichlet":
        g2s_method = g2s_dirichlet
    elif args.g2s_method.lower() == "g2s_weighted":
        g2s_method = g2s_weighted
    else:
        print("Unknown g2s method specified (%s)." % args.g2s_method, file=sys.stderr)
        exit(1)

    overwrite = not args.no_overwrite

    files_to_be_processed = []
    for f in args.files:
        # If a directory is specified, assume that its contents are filled with cthulhu-compatible
        # files to be processed.
        if os.path.isdir(f):
            for x in glob.glob("{}/*".format(f)):
                files_to_be_processed.append(x)
        # If a filename ends with .txt, assume that is contains paths to more files.
        elif os.path.splitext(f)[1] == ".txt":
            with open(f) as f2:
                for x in f2.readlines():
                    path = x.strip()
                    # Check that the line is not empty.
                    if path != "":
                        files_to_be_processed.append(path)
        else:
            files_to_be_processed.append(f)

    if args.progress and args.verbosity > 1:
        args.progress = False
        print("Cannot use --progress with verbosity > 1!", file=sys.stderr)
        exit(1)

    if args.progress and args.verbosity <= 1:
        pbar = tqdm(total=len(files_to_be_processed), desc="Running cthulhu")
    pool = mp.Pool(processes=args.processes)
    for result in pool.imap(unpack_model_plot, sorted(files_to_be_processed)):
        if result is not None:
            print(result)
        if args.progress:
            pbar.update(1)
    if args.progress and args.verbosity <= 1:
        pbar.close()
    pool.close()
