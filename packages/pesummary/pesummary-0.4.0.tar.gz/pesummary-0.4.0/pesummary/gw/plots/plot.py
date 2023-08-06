# Copyright (C) 2018  Charlie Hoy <charlie.hoy@ligo.org>
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from pesummary.utils.utils import logger, number_of_columns_for_legend
from pesummary.gw.plots.bounds import default_bounds
from pesummary.core.plots.kde import kdeplot
from pesummary import conf

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import corner

import numpy as np
import math
from scipy.ndimage import gaussian_filter
from astropy.time import Time
from gwpy.timeseries import TimeSeries
from gwpy.plot.colors import GW_OBSERVATORY_COLORS

from lal import MSUN_SI, PC_SI
try:
    import lalsimulation as lalsim
    LALSIMULATION = True
except ImportError:
    LALSIMULATION = None


def _1d_histogram_plot(param, samples, latex_label, inj_value=None, kde=False,
                       prior=None, weights=None):
    """Generate the 1d histogram plot for a given parameter for a given
    approximant.

    Parameters
    ----------
    param: str
        name of the parameter that you wish to plot
    samples: list
        list of samples for param
    latex_label: str
        latex label for param
    inj_value: float
        value that was injected
    kde: Bool
        if true, a kde is plotted instead of a histogram
    prior: list
        list of prior samples for param
    weights: list
        list of weights for each sample
    """
    logger.debug("Generating the 1d histogram plot for %s" % (param))
    xlow = np.min(samples)
    xhigh = np.max(samples)
    if param in default_bounds.keys():
        bounds = default_bounds[param]
        if "low" in bounds.keys():
            xlow = bounds["low"]
        if "high" in bounds.keys():
            if isinstance(bounds["high"], str) and "mass_1" in bounds["high"]:
                xhigh = np.max(samples)
            else:
                xhigh = bounds["high"]
    fig = plt.figure()
    if np.ptp(samples) == 0:
        plt.axvline(samples[0], color=conf.color)
        xlims = plt.gca().get_xlim()
    elif not kde:
        plt.hist(samples, histtype="step", bins=50, color=conf.color,
                 density=True, linewidth=1.75, weights=weights)
        xlims = plt.gca().get_xlim()
        if prior is not None:
            plt.hist(prior, color=conf.prior_color, alpha=0.2, edgecolor="w",
                     density=True, linewidth=1.75, histtype="bar", bins=50)
    else:
        x = kdeplot(
            samples, color=conf.color, shade=True, alpha_shade=0.1,
            linewidth=1.0, xlow=xlow, xhigh=xhigh
        )
        xlims = plt.gca().get_xlim()
        if prior is not None:
            kdeplot(prior, color=conf.prior_color, shade=True, alpha_shade=0.1,
                    linewidth=1.0, xlow=xlow, xhigh=xhigh)
    plt.xlabel(latex_label, fontsize=16)
    plt.ylabel("Probability Density", fontsize=16)
    percentile = samples.confidence_interval([5, 95])
    if inj_value is not None:
        plt.axvline(inj_value, color=conf.injection_color, linestyle='-',
                    linewidth=2.5)
    plt.axvline(percentile[0], color=conf.color, linestyle='--', linewidth=1.75)
    plt.axvline(percentile[1], color=conf.color, linestyle='--', linewidth=1.75)
    median = samples.average("median")
    upper = np.round(percentile[1] - median, 2)
    lower = np.round(median - percentile[0], 2)
    median = np.round(median, 2)
    plt.title(r"$%s^{+%s}_{-%s}$" % (median, upper, lower), fontsize=18)
    plt.grid(b=True)
    plt.xlim(xlims)
    plt.tight_layout()
    return fig


def _1d_comparison_histogram_plot(param, samples, colors,
                                  latex_label, labels, kde=False,
                                  linestyles=None):
    """Generate the a plot to compare the 1d_histogram plots for a given
    parameter for different approximants.

    Parameters
    ----------
    param: str
        name of the parameter that you wish to plot
    approximants: list
        list of approximant names that you would like to compare
    samples: 2d list
        list of samples for param for each approximant
    colors: list
        list of colors to be used to differentiate the different approximants
    latex_label: str
        latex label for param
    approximant_labels: list, optional
        label to prepend the approximant in the legend
    kde: Bool
        if true, a kde is plotted instead of a histogram
    linestyles: list
        list of linestyles for each set of samples
    """
    logger.debug("Generating the 1d comparison histogram plot for %s" % (param))
    xlow = None
    xhigh = None
    if param in default_bounds.keys():
        bounds = default_bounds[param]
        if "low" in bounds.keys():
            xlow = bounds["low"]
        if "high" in bounds.keys():
            if isinstance(bounds["high"], str) and "mass_1" in bounds["high"]:
                xhigh = np.max([np.max(i) for i in samples])
            else:
                xhigh = bounds["high"]
    if linestyles is None:
        linestyles = ["-"] * len(samples)
    fig = plt.figure(figsize=(8, 6))
    handles = []
    for num, i in enumerate(samples):
        if np.ptp(i) == 0:
            plt.axvline(i[0], color=colors[num], label=labels[num])
        elif not kde:
            plt.hist(i, histtype="step", bins=50, color=colors[num],
                     label=labels[num], linewidth=2.5, density=True,
                     linestyle=linestyles[num])
        else:
            kdeplot(i, color=colors[num], shade=True, alpha_shade=0.05,
                    linewidth=1.5, xlow=xlow, xhigh=xhigh, label=labels[num])
        plt.axvline(x=np.percentile(i, 95), color=colors[num], linestyle='--',
                    linewidth=2.5)
        plt.axvline(x=np.percentile(i, 5), color=colors[num], linestyle='--',
                    linewidth=2.5)
        handles.append(
            mlines.Line2D([], [], color=colors[num], label=labels[num])
        )
    ncols = number_of_columns_for_legend(labels)
    legend = plt.legend(
        handles=handles, bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        handlelength=3, ncol=ncols, mode="expand", borderaxespad=0.
    )
    for num, legobj in enumerate(legend.legendHandles):
        legobj.set_linewidth(1.75)
        legobj.set_linestyle(linestyles[num])
    plt.xlabel(latex_label, fontsize=16)
    plt.ylabel("Probability Density", fontsize=16)
    plt.grid(b=True)
    plt.tight_layout()
    return fig


def _make_corner_plot(samples, latex_labels, **kwargs):
    """Generate the corner plots for a given approximant

    Parameters
    ----------
    opts: argparse
        argument parser object to hold all information from the command line
    samples: nd list
        nd list of samples for each parameter for a given approximant
    params: list
        list of parameters associated with each element in samples
    approximant: str
        name of approximant that was used to generate the samples
    latex_labels: dict
        dictionary of latex labels for each parameter
    """
    logger.debug("Generating the corner plot")
    # set the default kwargs
    default_kwargs = dict(
        bins=50, smooth=0.9, label_kwargs=dict(fontsize=16),
        title_kwargs=dict(fontsize=16), color='#0072C1',
        truth_color='tab:orange', quantiles=[0.16, 0.84],
        levels=(1 - np.exp(-0.5), 1 - np.exp(-2), 1 - np.exp(-9 / 2.)),
        plot_density=False, plot_datapoints=True, fill_contours=True,
        max_n_ticks=3)
    parameters = list(samples.keys())
    corner_parameters = [
        "luminosity_distance", "dec", "a_2", "a_1", "geocent_time", "phi_jl",
        "psi", "ra", "phase", "mass_2", "mass_1", "phi_12", "tilt_2", "iota",
        "tilt_1", "chi_p", "chirp_mass", "mass_ratio", "symmetric_mass_ratio",
        "total_mass", "chi_eff", "redshift", "mass_1_source", "mass_2_source",
        "total_mass_source", "chirp_mass_source", "lambda_1", "lambda_2",
        "delta_lambda", "lambda_tilde"]
    included_parameters = [i for i in parameters if i in corner_parameters]
    xs = np.zeros([len(included_parameters), len(samples[parameters[0]])])
    for num, i in enumerate(included_parameters):
        xs[num] = samples[i]
    default_kwargs['range'] = [1.0] * len(included_parameters)
    default_kwargs["labels"] = [latex_labels[i] for i in included_parameters]
    figure = corner.corner(xs.T, **default_kwargs)
    # grab the axes of the subplots
    axes = figure.get_axes()
    axes_of_interest = axes[:2]
    location = []
    for i in axes_of_interest:
        extent = i.get_window_extent().transformed(
            figure.dpi_scale_trans.inverted()
        )
        location.append([extent.x0 * figure.dpi, extent.y0 * figure.dpi])
    width, height = extent.width, extent.height
    width *= figure.dpi
    height *= figure.dpi
    seperation = abs(location[0][0] - location[1][0]) - width
    data = {
        "width": width, "height": height, "seperation": seperation,
        "x0": location[0][0], "y0": location[0][0]
    }
    return figure, included_parameters, data


def _make_source_corner_plot(samples, latex_labels, **kwargs):
    """Generate the corner plots for a given approximant

    Parameters
    ----------
    opts: argparse
        argument parser object to hold all information from the command line
    samples: nd list
        nd list of samples for each parameter for a given approximant
    params: list
        list of parameters associated with each element in samples
    approximant: str
        name of approximant that was used to generate the samples
    latex_labels: dict
        dictionary of latex labels for each parameter
    """
    default_kwargs = dict(
        bins=50, smooth=0.9, label_kwargs=dict(fontsize=16),
        title_kwargs=dict(fontsize=16), color='#0072C1',
        truth_color='tab:orange', quantiles=[0.16, 0.84],
        levels=(1 - np.exp(-0.5), 1 - np.exp(-2), 1 - np.exp(-9 / 2.)),
        plot_density=False, plot_datapoints=True, fill_contours=True,
        max_n_ticks=3)
    parameters = list(samples.keys())
    corner_parameters = [
        "luminosity_distance", "mass_1_source", "mass_2_source",
        "total_mass_source", "chirp_mass_source", "redshift"]
    source_parameters = [i for i in parameters if i in corner_parameters]
    xs = np.zeros([len(source_parameters), len(samples[parameters[0]])])
    for num, i in enumerate(source_parameters):
        xs[num] = samples[i]
    default_kwargs['range'] = [1.0] * len(source_parameters)
    default_kwargs["labels"] = [latex_labels[i] for i in source_parameters]
    figure = corner.corner(xs.T, **default_kwargs)
    return figure


def _make_extrinsic_corner_plot(samples, latex_labels, **kwargs):
    """Generate the corner plots for a given approximant

    Parameters
    ----------
    opts: argparse
        argument parser object to hold all information from the command line
    samples: nd list
        nd list of samples for each parameter for a given approximant
    params: list
        list of parameters associated with each element in samples
    approximant: str
        name of approximant that was used to generate the samples
    latex_labels: dict
        dictionary of latex labels for each parameter
    """
    default_kwargs = dict(
        bins=50, smooth=0.9, label_kwargs=dict(fontsize=16),
        title_kwargs=dict(fontsize=16), color='#0072C1',
        truth_color='tab:orange', quantiles=[0.16, 0.84],
        levels=(1 - np.exp(-0.5), 1 - np.exp(-2), 1 - np.exp(-9 / 2.)),
        plot_density=False, plot_datapoints=True, fill_contours=True,
        max_n_ticks=3)
    parameters = list(samples.keys())
    corner_parameters = ["luminosity_distance", "psi", "ra", "dec"]
    extrinsic_parameters = [i for i in parameters if i in corner_parameters]
    xs = np.zeros([len(extrinsic_parameters), len(samples[parameters[0]])])
    for num, i in enumerate(extrinsic_parameters):
        xs[num] = samples[i]
    default_kwargs['range'] = [1.0] * len(extrinsic_parameters)
    default_kwargs["labels"] = [latex_labels[i] for i in extrinsic_parameters]
    figure = corner.corner(xs.T, **default_kwargs)
    return figure


def __antenna_response(name, ra, dec, psi, time_gps):
    """Calculate the antenna response function

    Parameters
    ----------
    name: str
        name of the detector you wish to calculate the antenna response
        function for
    ra: float
        right ascension of the source
    dec: float
        declination of the source
    psi: float
        polarisation of the source
    time_gps: float
        gps time of merger
    """
    gmst = Time(time_gps, format='gps', location=(0, 0))
    corrected_ra = gmst.sidereal_time('mean').rad - ra
    if not LALSIMULATION:
        raise Exception("lalsimulation could not be imported. please install "
                        "lalsuite to be able to use all features")
    detector = lalsim.DetectorPrefixToLALDetector(str(name))

    x0 = -np.cos(psi) * np.sin(corrected_ra) - \
        np.sin(psi) * np.cos(corrected_ra) * np.sin(dec)
    x1 = -np.cos(psi) * np.cos(corrected_ra) + \
        np.sin(psi) * np.sin(corrected_ra) * np.sin(dec)
    x2 = np.sin(psi) * np.cos(dec)
    x = np.array([x0, x1, x2])
    dx = detector.response.dot(x)

    y0 = np.sin(psi) * np.sin(corrected_ra) - \
        np.cos(psi) * np.cos(corrected_ra) * np.sin(dec)
    y1 = np.sin(psi) * np.cos(corrected_ra) + \
        np.cos(psi) * np.sin(corrected_ra) * np.sin(dec)
    y2 = np.cos(psi) * np.cos(dec)
    y = np.array([y0, y1, y2])
    dy = detector.response.dot(y)

    fplus = (x * dx - y * dy).sum()
    fcross = (x * dy + y * dx).sum()

    return fplus, fcross


def _waveform_plot(detectors, maxL_params, **kwargs):
    """Plot the maximum likelihood waveform for a given approximant.

    Parameters
    ----------
    detectors: list
        list of detectors that you want to generate waveforms for
    maxL_params: dict
        dictionary of maximum likelihood parameter values
    kwargs: dict
        dictionary of optional keyword arguments
    """
    if math.isnan(maxL_params["mass_1"]):
        return
    logger.debug("Generating the maximum likelihood waveform plot")
    if not LALSIMULATION:
        raise Exception("lalsimulation could not be imported. please install "
                        "lalsuite to be able to use all features")
    delta_frequency = kwargs.get("delta_f", 1. / 256)
    minimum_frequency = kwargs.get("f_min", 5.)
    maximum_frequency = kwargs.get("f_max", 1000.)
    frequency_array = np.arange(minimum_frequency, maximum_frequency,
                                delta_frequency)

    approx = lalsim.GetApproximantFromString(maxL_params["approximant"])
    mass_1 = maxL_params["mass_1"] * MSUN_SI
    mass_2 = maxL_params["mass_2"] * MSUN_SI
    luminosity_distance = maxL_params["luminosity_distance"] * PC_SI * 10**6
    if "phi_jl" in maxL_params.keys():
        iota, S1x, S1y, S1z, S2x, S2y, S2z = \
            lalsim.SimInspiralTransformPrecessingNewInitialConditions(
                maxL_params["theta_jn"], maxL_params["phi_jl"], maxL_params["tilt_1"],
                maxL_params["tilt_2"], maxL_params["phi_12"], maxL_params["a_1"],
                maxL_params["a_2"], mass_1, mass_2, kwargs.get("f_ref", 10.),
                maxL_params["phase"])
    else:
        iota, S1x, S1y, S1z, S2x, S2y, S2z = maxL_params["iota"], 0., 0., 0., \
            0., 0., 0.
    phase = maxL_params["phase"] if "phase" in maxL_params.keys() else 0.0
    h_plus, h_cross = lalsim.SimInspiralChooseFDWaveform(
        mass_1, mass_2, S1x, S1y, S1z, S2x, S2y, S2z, luminosity_distance, iota,
        phase, 0.0, 0.0, 0.0, delta_frequency, minimum_frequency,
        maximum_frequency, kwargs.get("f_ref", 10.), None, approx)
    h_plus = h_plus.data.data
    h_cross = h_cross.data.data
    h_plus = h_plus[:len(frequency_array)]
    h_cross = h_cross[:len(frequency_array)]
    fig = plt.figure()
    colors = [GW_OBSERVATORY_COLORS[i] for i in detectors]
    for num, i in enumerate(detectors):
        ar = __antenna_response(i, maxL_params["ra"], maxL_params["dec"],
                                maxL_params["psi"], maxL_params["geocent_time"])
        plt.plot(frequency_array, abs(h_plus * ar[0] + h_cross * ar[1]),
                 color=colors[num], linewidth=1.0, label=i)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel(r"Frequency $[Hz]$", fontsize=16)
    plt.ylabel(r"Strain", fontsize=16)
    plt.grid(b=True)
    plt.legend(loc="best")
    plt.tight_layout()
    return fig


def _waveform_comparison_plot(maxL_params_list, colors, labels,
                              **kwargs):
    """Generate a plot which compares the maximum likelihood waveforms for
    each approximant.

    Parameters
    ----------
    maxL_params_list: list
        list of dictionaries containing the maximum likelihood parameter
        values for each approximant
    colors: list
        list of colors to be used to differentiate the different approximants
    approximant_labels: list, optional
        label to prepend the approximant in the legend
    kwargs: dict
        dictionary of optional keyword arguments
    """
    logger.debug("Generating the maximum likelihood waveform comparison plot "
                 "for H1")
    if not LALSIMULATION:
        raise Exception("LALSimulation could not be imported. Please install "
                        "LALSuite to be able to use all features")
    delta_frequency = kwargs.get("delta_f", 1. / 256)
    minimum_frequency = kwargs.get("f_min", 5.)
    maximum_frequency = kwargs.get("f_max", 1000.)
    frequency_array = np.arange(minimum_frequency, maximum_frequency,
                                delta_frequency)

    fig = plt.figure()
    for num, i in enumerate(maxL_params_list):
        if math.isnan(i["mass_1"]):
            continue
        approx = lalsim.GetApproximantFromString(i["approximant"])
        mass_1 = i["mass_1"] * MSUN_SI
        mass_2 = i["mass_2"] * MSUN_SI
        luminosity_distance = i["luminosity_distance"] * PC_SI * 10**6
        if "phi_jl" in i.keys():
            iota, S1x, S1y, S1z, S2x, S2y, S2z = \
                lalsim.SimInspiralTransformPrecessingNewInitialConditions(
                    i["theta_jn"], i["phi_jl"], i["tilt_1"],
                    i["tilt_2"], i["phi_12"], i["a_1"],
                    i["a_2"], mass_1, mass_2, kwargs.get("f_ref", 10.),
                    i["phase"])
        else:
            iota, S1x, S1y, S1z, S2x, S2y, S2z = i["iota"], 0., 0., 0., \
                0., 0., 0.
        phase = i["phase"] if "phase" in i.keys() else 0.0
        h_plus, h_cross = lalsim.SimInspiralChooseFDWaveform(
            mass_1, mass_2, S1x, S1y, S1z, S2x, S2y, S2z, luminosity_distance,
            iota, phase, 0.0, 0.0, 0.0, delta_frequency, minimum_frequency,
            maximum_frequency, kwargs.get("f_ref", 10.), None, approx)
        h_plus = h_plus.data.data
        h_cross = h_cross.data.data
        h_plus = h_plus[:len(frequency_array)]
        h_cross = h_cross[:len(frequency_array)]
        ar = __antenna_response("H1", i["ra"], i["dec"], i["psi"],
                                i["geocent_time"])
        plt.plot(frequency_array, abs(h_plus * ar[0] + h_cross * ar[1]),
                 color=colors[num], label=labels[num], linewidth=2.0)
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(b=True)
    plt.legend(loc="best")
    plt.xlabel(r"Frequency $[Hz]$", fontsize=16)
    plt.ylabel(r"Strain", fontsize=16)
    plt.tight_layout()
    return fig


def _ligo_skymap_plot(ra, dec, dist=None, savedir="./", nprocess=1,
                      downsampled=False, label="pesummary",
                      distance_map=True, multi_resolution=True, **kwargs):
    """Plot the sky location of the source for a given approximant using the
    ligo.skymap package

    Parameters
    ----------
    ra: list
        list of samples for right ascension
    dec: list
        list of samples for declination
    dist: list
        list of samples for the luminosity distance
    savedir: str
        path to the directory where you would like to save the output files
    nprocess: Bool
        Boolean for whether to use multithreading or not
    downsampled: Bool
        Boolean for whether the samples have been downsampled or not
    distance_map: Bool
        Boolean for whether or not to produce a distance map
    multi_resolution: Bool
        Boolean for whether or not to generate a multiresolution HEALPix map
    kwargs: dict
        optional keyword arguments
    """
    import healpy as hp
    from ligo.skymap import plot, postprocess, io
    from ligo.skymap.bayestar import rasterize
    from ligo.skymap.kde import Clustered2DSkyKDE, Clustered2Plus1DSkyKDE
    from astropy.time import Time

    fig = plt.figure()
    if dist is not None and distance_map:
        pts = np.column_stack((ra, dec, dist))
        cls = Clustered2Plus1DSkyKDE
    else:
        pts = np.column_stack((ra, dec))
        cls = Clustered2DSkyKDE
    skypost = cls(pts, trials=5, jobs=nprocess)
    hpmap = skypost.as_healpix()
    if not multi_resolution:
        hpmap = rasterize(hpmap)
    hpmap.meta['creator'] = "pesummary"
    hpmap.meta['origin'] = 'LIGO/Virgo'
    hpmap.meta['gps_creation_time'] = Time.now().gps
    if dist is not None:
        hpmap.meta["distmean"] = float(np.mean(dist))
        hpmap.meta["diststd"] = float(np.std(dist))
    io.write_sky_map(
        os.path.join(savedir, "%s_skymap.fits" % (label)), hpmap, nest=True
    )
    skymap, metadata = io.fits.read_sky_map(
        os.path.join(savedir, "%s_skymap.fits" % (label)), nest=None
    )
    nside = hp.npix2nside(len(skymap))
    deg2perpix = hp.nside2pixarea(nside, degrees=True)
    probperdeg2 = skymap / deg2perpix

    ax = plt.axes(projection='astro hours mollweide')
    ax.grid(b=True)
    if downsampled:
        ax.set_title("Downsampled to %s" % (len(ra)), fontdict={'fontsize': 11})

    vmax = probperdeg2.max()
    ax.imshow_hpx((probperdeg2, 'ICRS'), nested=True, vmin=0.,
                  vmax=vmax, cmap="cylon")
    cls = 100 * postprocess.find_greedy_credible_levels(skymap)
    cs = ax.contour_hpx((cls, 'ICRS'), nested=True, colors='k',
                        linewidths=0.5, levels=[50, 90])
    plt.clabel(cs, fmt=r'%g\%%', fontsize=6, inline=True)
    text = []
    pp = np.round([50, 90]).astype(int)
    ii = np.round(
        np.searchsorted(np.sort(cls), [50, 90]) * deg2perpix).astype(int)
    for i, p in zip(ii, pp):
        text.append(u'{:d}% area: {:d} deg²'.format(p, i, grouping=True))
    ax.text(1, 1.05, '\n'.join(text), transform=ax.transAxes, ha='right',
            fontsize=10)
    plot.outline_text(ax)
    return fig


def _default_skymap_plot(ra, dec, weights=None, **kwargs):
    """Plot the default sky location of the source for a given approximant

    Parameters
    ----------
    ra: list
        list of samples for right ascension
    dec: list
        list of samples for declination
    kwargs: dict
        optional keyword arguments
    """
    ra = [-i + np.pi for i in ra]
    logger.debug("Generating the sky map plot")
    fig = plt.figure()
    ax = plt.subplot(111, projection="mollweide",
                     facecolor=(1.0, 0.939165516411, 0.880255669068))
    ax.cla()
    ax.set_title("Preliminary", fontdict={'fontsize': 11})
    ax.grid(b=True)
    ax.set_xticklabels([
        r"$2^{h}$", r"$4^{h}$", r"$6^{h}$", r"$8^{h}$", r"$10^{h}$",
        r"$12^{h}$", r"$14^{h}$", r"$16^{h}$", r"$18^{h}$", r"$20^{h}$",
        r"$22^{h}$"])
    levels = [0.9, 0.5]

    if weights is None:
        H, X, Y = np.histogram2d(ra, dec, bins=50)
    else:
        H, X, Y = np.histogram2d(ra, dec, bins=50, weights=weights)
    H = gaussian_filter(H, kwargs.get("smooth", 0.9))
    Hflat = H.flatten()
    indicies = np.argsort(Hflat)[::-1]
    Hflat = Hflat[indicies]

    CF = np.cumsum(Hflat)
    CF /= CF[-1]

    V = np.empty(len(levels))
    for num, i in enumerate(levels):
        try:
            V[num] = Hflat[CF <= i][-1]
        except Exception:
            V[num] = Hflat[0]
    V.sort()
    m = np.diff(V) == 0
    while np.any(m):
        V[np.where(m)[0][0]] *= 1.0 - 1e-4
        m = np.diff(V) == 0
    V.sort()
    X1, Y1 = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1])

    H2 = H.min() + np.zeros((H.shape[0] + 4, H.shape[1] + 4))
    H2[2:-2, 2:-2] = H
    H2[2:-2, 1] = H[:, 0]
    H2[2:-2, -2] = H[:, -1]
    H2[1, 2:-2] = H[0]
    H2[-2, 2:-2] = H[-1]
    H2[1, 1] = H[0, 0]
    H2[1, -2] = H[0, -1]
    H2[-2, 1] = H[-1, 0]
    H2[-2, -2] = H[-1, -1]
    X2 = np.concatenate([X1[0] + np.array([-2, -1]) * np.diff(X1[:2]), X1,
                         X1[-1] + np.array([1, 2]) * np.diff(X1[-2:]), ])
    Y2 = np.concatenate([Y1[0] + np.array([-2, -1]) * np.diff(Y1[:2]), Y1,
                         Y1[-1] + np.array([1, 2]) * np.diff(Y1[-2:]), ])

    ax.pcolormesh(X2, Y2, H2.T, vmin=0., vmax=H2.T.max(), cmap="cylon")
    cs = plt.contour(X2, Y2, H2.T, V, colors="k", linewidths=0.5)
    fmt = {l: s for l, s in zip(cs.levels, [r"$90\%$", r"$50\%$"])}
    plt.clabel(cs, fmt=fmt, fontsize=8, inline=True)
    text = []
    for i, j in zip(cs.collections, [90, 50]):
        area = 0.
        for k in i.get_paths():
            x = k.vertices[:, 0]
            y = k.vertices[:, 1]
            area += 0.5 * np.sum(y[:-1] * np.diff(x) - x[:-1] * np.diff(y))
        area = int(np.abs(area) * (180 / np.pi) * (180 / np.pi))
        text.append(u'{:d}% area: {:d} deg²'.format(
            int(j), area, grouping=True))
    ax.text(1, 1.05, '\n'.join(text[::-1]), transform=ax.transAxes, ha='right',
            fontsize=10)
    xticks = np.arange(-np.pi, np.pi + np.pi / 6, np.pi / 4)
    ax.set_xticks(xticks)
    ax.set_yticks([-np.pi / 3, -np.pi / 6, 0, np.pi / 6, np.pi / 3])
    labels = [r"$%s^{h}$" % (int(np.round((i + np.pi) * 3.82, 1))) for i in xticks]
    ax.set_xticklabels(labels[::-1], fontsize=10)
    ax.set_yticklabels([r"$-60^\degree$", r"$-30^\degree$", r"$0^\degree$",
                        r"$30^\degree$", r"$60^\degree$"], fontsize=10)
    ax.grid(b=True)
    return fig


def _sky_map_comparison_plot(ra_list, dec_list, labels, colors, **kwargs):
    """Generate a plot that compares the sky location for multiple approximants

    Parameters
    ----------
    ra_list: 2d list
        list of samples for right ascension for each approximant
    dec_list: 2d list
        list of samples for declination for each approximant
    approximants: list
        list of approximants used to generate the samples
    colors: list
        list of colors to be used to differentiate the different approximants
    approximant_labels: list, optional
        label to prepend the approximant in the legend
    kwargs: dict
        optional keyword arguments
    """
    ra_list = [[-i + np.pi for i in j] for j in ra_list]
    logger.debug("Generating the sky map comparison plot")
    fig = plt.figure()
    ax = plt.subplot(111, projection="mollweide",
                     facecolor=(1.0, 0.939165516411, 0.880255669068))
    ax.cla()
    ax.grid(b=True)
    ax.set_xticklabels([
        r"$2^{h}$", r"$4^{h}$", r"$6^{h}$", r"$8^{h}$", r"$10^{h}$",
        r"$12^{h}$", r"$14^{h}$", r"$16^{h}$", r"$18^{h}$", r"$20^{h}$",
        r"$22^{h}$"])
    levels = [0.9, 0.5]
    for num, i in enumerate(ra_list):
        H, X, Y = np.histogram2d(i, dec_list[num], bins=50)
        H = gaussian_filter(H, kwargs.get("smooth", 0.9))
        Hflat = H.flatten()
        indicies = np.argsort(Hflat)[::-1]
        Hflat = Hflat[indicies]

        CF = np.cumsum(Hflat)
        CF /= CF[-1]

        V = np.empty(len(levels))
        for num2, j in enumerate(levels):
            try:
                V[num2] = Hflat[CF <= j][-1]
            except Exception:
                V[num2] = Hflat[0]
        V.sort()
        m = np.diff(V) == 0
        while np.any(m):
            V[np.where(m)[0][0]] *= 1.0 - 1e-4
            m = np.diff(V) == 0
        V.sort()
        X1, Y1 = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1])

        H2 = H.min() + np.zeros((H.shape[0] + 4, H.shape[1] + 4))
        H2[2:-2, 2:-2] = H
        H2[2:-2, 1] = H[:, 0]
        H2[2:-2, -2] = H[:, -1]
        H2[1, 2:-2] = H[0]
        H2[-2, 2:-2] = H[-1]
        H2[1, 1] = H[0, 0]
        H2[1, -2] = H[0, -1]
        H2[-2, 1] = H[-1, 0]
        H2[-2, -2] = H[-1, -1]
        X2 = np.concatenate([X1[0] + np.array([-2, -1]) * np.diff(X1[:2]), X1,
                             X1[-1] + np.array([1, 2]) * np.diff(X1[-2:]), ])
        Y2 = np.concatenate([Y1[0] + np.array([-2, -1]) * np.diff(Y1[:2]), Y1,
                             Y1[-1] + np.array([1, 2]) * np.diff(Y1[-2:]), ])
        CS = plt.contour(X2, Y2, H2.T, V, colors=colors[num], linewidths=2.0)
        CS.collections[0].set_label(labels[num])
    ncols = number_of_columns_for_legend(labels)
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, borderaxespad=0.,
               mode="expand", ncol=ncols)
    xticks = np.arange(-np.pi, np.pi + np.pi / 6, np.pi / 4)
    ax.set_xticks(xticks)
    ax.set_yticks([-np.pi / 3, -np.pi / 6, 0, np.pi / 6, np.pi / 3])
    labels = [r"$%s^{h}$" % (int(np.round((i + np.pi) * 3.82, 1))) for i in xticks]
    ax.set_xticklabels(labels[::-1], fontsize=10)
    ax.set_yticklabels([r"$-60^\degree$", r"$-30^\degree$", r"$0^\degree$",
                        r"$30^\degree$", r"$60^\degree$"], fontsize=10)
    ax.grid(b=True)
    return fig


def __get_cutoff_indices(flow, fhigh, df, N):
    """
    Gets the indices of a frequency series at which to stop an overlap
    calculation.

    Parameters
    ----------
    flow: float
        The frequency (in Hz) of the lower index.
    fhigh: float
        The frequency (in Hz) of the upper index.
    df: float
        The frequency step (in Hz) of the frequency series.
    N: int
        The number of points in the **time** series. Can be odd
        or even.

    Returns
    -------
    kmin: int
    kmax: int
    """
    if flow:
        kmin = int(flow / df)
    else:
        kmin = 1
    if fhigh:
        kmax = int(fhigh / df)
    else:
        kmax = int((N + 1) / 2.)
    return kmin, kmax


def _sky_sensitivity(network, resolution, maxL_params, **kwargs):
    """Generate the sky sensitivity for a given network

    Parameters
    ----------
    network: list
        list of detectors you want included in your sky sensitivity plot
    resolution: float
        resolution of the skymap
    maxL_params: dict
        dictionary of waveform parameters for the maximum likelihood waveform
    """
    logger.debug("Generating the sky sensitivity for %s" % (network))
    if not LALSIMULATION:
        raise Exception("LALSimulation could not be imported. Please install "
                        "LALSuite to be able to use all features")
    delta_frequency = kwargs.get("delta_f", 1. / 256)
    minimum_frequency = kwargs.get("f_min", 20.)
    maximum_frequency = kwargs.get("f_max", 1000.)
    frequency_array = np.arange(minimum_frequency, maximum_frequency,
                                delta_frequency)

    approx = lalsim.GetApproximantFromString(maxL_params["approximant"])
    mass_1 = maxL_params["mass_1"] * MSUN_SI
    mass_2 = maxL_params["mass_2"] * MSUN_SI
    luminosity_distance = maxL_params["luminosity_distance"] * PC_SI * 10**6
    iota, S1x, S1y, S1z, S2x, S2y, S2z = \
        lalsim.SimInspiralTransformPrecessingNewInitialConditions(
            maxL_params["iota"], maxL_params["phi_jl"], maxL_params["tilt_1"],
            maxL_params["tilt_2"], maxL_params["phi_12"], maxL_params["a_1"],
            maxL_params["a_2"], mass_1, mass_2, kwargs.get("f_ref", 10.),
            maxL_params["phase"])
    h_plus, h_cross = lalsim.SimInspiralChooseFDWaveform(
        mass_1, mass_2, S1x, S1y, S1z, S2x, S2y, S2z, luminosity_distance, iota,
        maxL_params["phase"], 0.0, 0.0, 0.0, delta_frequency, minimum_frequency,
        maximum_frequency, kwargs.get("f_ref", 10.), None, approx)
    h_plus = h_plus.data.data
    h_cross = h_cross.data.data
    h_plus = h_plus[:len(frequency_array)]
    h_cross = h_cross[:len(frequency_array)]
    psd = {}
    psd["H1"] = psd["L1"] = np.array([
        lalsim.SimNoisePSDaLIGOZeroDetHighPower(i) for i in frequency_array])
    psd["V1"] = np.array([lalsim.SimNoisePSDVirgo(i) for i in frequency_array])
    kmin, kmax = __get_cutoff_indices(minimum_frequency, maximum_frequency,
                                      delta_frequency, (len(h_plus) - 1) * 2)
    ra = np.arange(-np.pi, np.pi, resolution)
    dec = np.arange(-np.pi, np.pi, resolution)
    X, Y = np.meshgrid(ra, dec)
    N = np.zeros([len(dec), len(ra)])

    indices = np.ndindex(len(ra), len(dec))
    for ind in indices:
        ar = {}
        SNR = {}
        for i in network:
            ard = __antenna_response(i, ra[ind[0]], dec[ind[1]],
                                     maxL_params["psi"], maxL_params["geocent_time"])
            ar[i] = [ard[0], ard[1]]
            strain = np.array(h_plus * ar[i][0] + h_cross * ar[i][1])
            integrand = np.conj(strain[kmin:kmax]) * strain[kmin:kmax] / psd[i][kmin:kmax]
            integrand = integrand[:-1]
            SNR[i] = np.sqrt(4 * delta_frequency * np.sum(integrand).real)
            ar[i][0] *= SNR[i]
            ar[i][1] *= SNR[i]
        numerator = 0.0
        denominator = 0.0
        for i in network:
            numerator += sum(i**2 for i in ar[i])
            denominator += SNR[i]**2
        N[ind[1]][ind[0]] = (((numerator / denominator)**0.5))
    fig = plt.figure()
    ax = plt.subplot(111, projection="hammer")
    ax.cla()
    ax.grid(b=True)
    plt.pcolormesh(X, Y, N)
    ax.set_xticklabels([
        r"$22^{h}$", r"$20^{h}$", r"$18^{h}$", r"$16^{h}$", r"$14^{h}$",
        r"$12^{h}$", r"$10^{h}$", r"$8^{h}$", r"$6^{h}$", r"$4^{h}$",
        r"$2^{h}$"])
    return fig


def _time_domain_waveform(detectors, maxL_params, **kwargs):
    """
    Plot the maximum likelihood waveform for a given approximant
    in the time domain.

    Parameters
    ----------
    detectors: list
        list of detectors that you want to generate waveforms for
    maxL_params: dict
        dictionary of maximum likelihood parameter values
    kwargs: dict
        dictionary of optional keyword arguments
    """
    if math.isnan(maxL_params["mass_1"]):
        return
    logger.debug("Generating the maximum likelihood waveform time domain plot")
    if not LALSIMULATION:
        raise Exception("lalsimulation could not be imported. please install "
                        "lalsuite to be able to use all features")
    delta_t = 1. / 4096.
    minimum_frequency = kwargs.get("f_min", 5.)
    t_start = maxL_params['geocent_time']
    t_finish = maxL_params['geocent_time'] + 4.
    time_array = np.arange(t_start, t_finish, delta_t)

    approx = lalsim.GetApproximantFromString(maxL_params["approximant"])
    mass_1 = maxL_params["mass_1"] * MSUN_SI
    mass_2 = maxL_params["mass_2"] * MSUN_SI
    luminosity_distance = maxL_params["luminosity_distance"] * PC_SI * 10**6
    if "phi_jl" in maxL_params.keys():
        iota, S1x, S1y, S1z, S2x, S2y, S2z = \
            lalsim.SimInspiralTransformPrecessingNewInitialConditions(
                maxL_params["theta_jn"], maxL_params["phi_jl"], maxL_params["tilt_1"],
                maxL_params["tilt_2"], maxL_params["phi_12"], maxL_params["a_1"],
                maxL_params["a_2"], mass_1, mass_2, kwargs.get("f_ref", 10.),
                maxL_params["phase"])
    else:
        iota, S1x, S1y, S1z, S2x, S2y, S2z = maxL_params["iota"], 0., 0., 0., \
            0., 0., 0.
    phase = maxL_params["phase"] if "phase" in maxL_params.keys() else 0.0
    h_plus, h_cross = lalsim.SimInspiralChooseTDWaveform(
        mass_1, mass_2, S1x, S1y, S1z, S2x, S2y, S2z, luminosity_distance, iota,
        phase, 0.0, 0.0, 0.0, delta_t, minimum_frequency,
        kwargs.get("f_ref", 10.), None, approx)

    fig = plt.figure()
    colors = [GW_OBSERVATORY_COLORS[i] for i in detectors]
    for num, i in enumerate(detectors):
        ar = __antenna_response(i, maxL_params["ra"], maxL_params["dec"],
                                maxL_params["psi"], maxL_params["geocent_time"])
        h_t = h_plus.data.data * ar[0] + h_cross.data.data * ar[1]
        h_t = TimeSeries(h_t[:], dt=h_plus.deltaT, t0=h_plus.epoch)
        h_t.times = [float(np.array(i)) + t_start for i in h_t.times]
        plt.plot(h_t.times, h_t,
                 color=colors[num], linewidth=1.0, label=i)
        plt.xlim([t_start - 3, t_start + 0.5])
    plt.xlabel(r"Time $[s]$", fontsize=16)
    plt.ylabel(r"Strain", fontsize=16)
    plt.grid(b=True)
    plt.legend(loc="best")
    plt.tight_layout()
    return fig


def _time_domain_waveform_comparison_plot(maxL_params_list, colors, labels,
                                          **kwargs):
    """Generate a plot which compares the maximum likelihood waveforms for
    each approximant.

    Parameters
    ----------
    maxL_params_list: list
        list of dictionaries containing the maximum likelihood parameter
        values for each approximant
    colors: list
        list of colors to be used to differentiate the different approximants
    approximant_labels: list, optional
        label to prepend the approximant in the legend
    kwargs: dict
        dictionary of optional keyword arguments
    """
    logger.debug("Generating the maximum likelihood time domain waveform "
                 "comparison plot for H1")
    if not LALSIMULATION:
        raise Exception("LALSimulation could not be imported. Please install "
                        "LALSuite to be able to use all features")
    delta_t = 1. / 4096.
    minimum_frequency = kwargs.get("f_min", 5.)

    fig = plt.figure()
    for num, i in enumerate(maxL_params_list):
        if math.isnan(i["mass_1"]):
            continue
        t_start = i['geocent_time']
        t_finish = i['geocent_time'] + 4.
        time_array = np.arange(t_start, t_finish, delta_t)

        approx = lalsim.GetApproximantFromString(i["approximant"])
        mass_1 = i["mass_1"] * MSUN_SI
        mass_2 = i["mass_2"] * MSUN_SI
        luminosity_distance = i["luminosity_distance"] * PC_SI * 10**6
        if "phi_jl" in i.keys():
            iota, S1x, S1y, S1z, S2x, S2y, S2z = \
                lalsim.SimInspiralTransformPrecessingNewInitialConditions(
                    i["theta_jn"], i["phi_jl"], i["tilt_1"],
                    i["tilt_2"], i["phi_12"], i["a_1"],
                    i["a_2"], mass_1, mass_2, kwargs.get("f_ref", 10.),
                    i["phase"])
        else:
            iota, S1x, S1y, S1z, S2x, S2y, S2z = i["iota"], 0., 0., 0., \
                0., 0., 0.
        phase = i["phase"] if "phase" in i.keys() else 0.0
        h_plus, h_cross = lalsim.SimInspiralChooseTDWaveform(
            mass_1, mass_2, S1x, S1y, S1z, S2x, S2y, S2z, luminosity_distance,
            iota, phase, 0.0, 0.0, 0.0, delta_t, minimum_frequency,
            kwargs.get("f_ref", 10.), None, approx)

        ar = __antenna_response("H1", i["ra"], i["dec"], i["psi"],
                                i["geocent_time"])
        h_t = h_plus.data.data * ar[0] + h_cross.data.data * ar[1]
        h_t = TimeSeries(h_t[:], dt=h_plus.deltaT, t0=h_plus.epoch)
        h_t.times = [float(np.array(i)) + t_start for i in h_t.times]

        plt.plot(h_t.times, h_t,
                 color=colors[num], label=labels[num], linewidth=2.0)
    plt.xlabel(r"Time $[s]$", fontsize=16)
    plt.ylabel(r"Strain", fontsize=16)
    plt.xlim([t_start - 3, t_start + 0.5])
    plt.grid(b=True)
    plt.legend(loc="best")
    plt.tight_layout()
    return fig


def _psd_plot(frequencies, strains, colors=None, labels=None, fmin=None):
    """Superimpose all PSD plots onto a single figure.

    Parameters
    ----------
    frequencies: nd list
        list of all frequencies used for each psd file
    strains: nd list
        list of all strains used for each psd file
    colors: optional, list
        list of colors to be used to differentiate the different PSDs
    labels: optional, list
        list of lavels for each PSD
    fmin: optional, float
        starting frequency of the plot
    """
    fig, ax = plt.subplots(1, 1)
    if not colors and all(i in GW_OBSERVATORY_COLORS.keys() for i in labels):
        colors = [GW_OBSERVATORY_COLORS[i] for i in labels]
    elif not colors:
        colors = ['r', 'b', 'orange', 'c', 'g', 'purple']
        while len(colors) <= len(labels):
            colors += colors
    for num, i in enumerate(frequencies):
        if fmin is not None:
            ff = np.array(i)
            ss = np.array(strains[num])
            ind = np.argwhere(ff >= fmin)
            i = ff[ind]
            strains[num] = ss[ind]
        plt.loglog(i, strains[num], color=colors[num], label=labels[num])
    ax.tick_params(which="both", bottom=True, length=3, width=1)
    ax.set_xlabel(r"Frequency $[Hz]$", fontsize=16)
    ax.set_ylabel(r"Strain Noise $[1/\sqrt{Hz}]$", fontsize=16)
    plt.legend(loc="best")
    plt.tight_layout()
    return fig


def _calibration_envelope_plot(frequency, calibration_envelopes, ifos,
                               colors=None, prior=[]):
    """Generate a plot showing the calibration envelope

    Parameters
    ----------
    frequency: array
        frequency bandwidth that you would like to use
    calibration_envelopes: nd list
        list containing the calibration envelope data for different IFOs
    ifos: list
        list of IFOs that are associated with the calibration envelopes
    colors: list, optional
        list of colors to be used to differentiate the different calibration
        envelopes
    prior: list, optional
        list containing the prior calibration envelope data for different IFOs
    """
    def interpolate_calibration(data):
        """Interpolate the calibration data using spline

        Parameters
        ----------
        data: np.ndarray
            array containing the calibration data
        """
        interp = [
            np.interp(frequency, data[:, 0], data[:, j], left=k, right=k)
            for j, k in zip(range(1, 7), [1, 0, 1, 0, 1, 0])
        ]
        amp_median = (1 - interp[0]) * 100
        phase_median = interp[1] * 180. / np.pi
        amp_lower_sigma = (1 - interp[2]) * 100
        phase_lower_sigma = interp[3] * 180. / np.pi
        amp_upper_sigma = (1 - interp[4]) * 100
        phase_upper_sigma = interp[5] * 180. / np.pi
        data_dict = {
            "amplitude": {
                "median": amp_median,
                "lower": amp_lower_sigma,
                "upper": amp_upper_sigma
            },
            "phase": {
                "median": phase_median,
                "lower": phase_lower_sigma,
                "upper": phase_upper_sigma
            }
        }
        return data_dict

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    if not colors and all(i in GW_OBSERVATORY_COLORS.keys() for i in ifos):
        colors = [GW_OBSERVATORY_COLORS[i] for i in ifos]
    elif not colors:
        colors = ['r', 'b', 'orange', 'c', 'g', 'purple']
        while len(colors) <= len(ifos):
            colors += colors

    for num, i in enumerate(calibration_envelopes):
        calibration_envelopes[num] = np.array(calibration_envelopes[num])

    for num, i in enumerate(calibration_envelopes):
        calibration_data = interpolate_calibration(i)
        if prior != []:
            prior_data = interpolate_calibration(prior[num])
        ax1.plot(
            frequency, calibration_data["amplitude"]["upper"], color=colors[num],
            linestyle="-", label=ifos[num]
        )
        ax1.plot(
            frequency, calibration_data["amplitude"]["lower"], color=colors[num],
            linestyle="-"
        )
        ax1.set_ylabel(r"Amplitude deviation $[\%]$")
        ax1.legend(loc="best")
        ax2.plot(
            frequency, calibration_data["phase"]["upper"], color=colors[num],
            linestyle="-", label=ifos[num]
        )
        ax2.plot(
            frequency, calibration_data["phase"]["lower"], color=colors[num],
            linestyle="-"
        )
        ax2.set_ylabel(r"Phase deviation $[\degree]$")
        if prior != []:
            ax1.fill_between(
                frequency, prior_data["amplitude"]["upper"],
                prior_data["amplitude"]["lower"], color=colors[num], alpha=0.2
            )
            ax2.fill_between(
                frequency, prior_data["phase"]["upper"],
                prior_data["phase"]["lower"], color=colors[num], alpha=0.2
            )

    plt.xscale('log')
    plt.xlabel(r"Frequency $[Hz]$", fontsize=16)
    plt.tight_layout()
    return fig


def _strain_plot(strain, maxL_params, **kwargs):
    """Generate a plot showing the strain data and the maxL waveform

    Parameters
    ----------
    strain: gwpy.timeseries
        timeseries containing the strain data
    maxL_samples: dict
        dictionary of maximum likelihood parameter values
    """
    logger.debug("Generating the strain plot")
    from pesummary.gw.file.conversions import time_in_each_ifo

    fig = plt.figure()
    time = maxL_params["geocent_time"]
    delta_t = 1. / 4096.
    minimum_frequency = kwargs.get("f_min", 5.)
    t_start = time - 15.0
    t_finish = time + 0.06
    time_array = np.arange(t_start, t_finish, delta_t)

    approx = lalsim.GetApproximantFromString(maxL_params["approximant"])
    mass_1 = maxL_params["mass_1"] * MSUN_SI
    mass_2 = maxL_params["mass_2"] * MSUN_SI
    luminosity_distance = maxL_params["luminosity_distance"] * PC_SI * 10**6
    if "phi_jl" in maxL_params.keys():
        iota, S1x, S1y, S1z, S2x, S2y, S2z = \
            lalsim.SimInspiralTransformPrecessingNewInitialConditions(
                maxL_params["theta_jn"], maxL_params["phi_jl"], maxL_params["tilt_1"],
                maxL_params["tilt_2"], maxL_params["phi_12"], maxL_params["a_1"],
                maxL_params["a_2"], mass_1, mass_2, kwargs.get("f_ref", 10.),
                maxL_params["phase"])
    else:
        iota, S1x, S1y, S1z, S2x, S2y, S2z = maxL_params["iota"], 0., 0., 0., \
            0., 0., 0.
    phase = maxL_params["phase"] if "phase" in maxL_params.keys() else 0.0
    h_plus, h_cross = lalsim.SimInspiralChooseTDWaveform(
        mass_1, mass_2, S1x, S1y, S1z, S2x, S2y, S2z, luminosity_distance, iota,
        phase, 0.0, 0.0, 0.0, delta_t, minimum_frequency,
        kwargs.get("f_ref", 10.), None, approx)

    for num, key in enumerate(list(strain.keys())):
        ifo_time = time_in_each_ifo(key, maxL_params["ra"], maxL_params["dec"],
                                    maxL_params["geocent_time"])

        asd = strain[key].asd(8, 4, method="median")
        strain_data_frequency = strain[key].fft()
        asd_interp = asd.interpolate(float(np.array(strain_data_frequency.df)))
        asd_interp = asd_interp[:len(strain_data_frequency)]
        strain_data_time = (strain_data_frequency / asd_interp).ifft()
        strain_data_time = strain_data_time.highpass(30)
        strain_data_time = strain_data_time.lowpass(300)

        ar = __antenna_response(key, maxL_params["ra"], maxL_params["dec"],
                                maxL_params["psi"], maxL_params["geocent_time"])

        h_t = ar[0] * h_plus.data.data + ar[1] * h_cross.data.data
        h_t = TimeSeries(h_t[:], dt=h_plus.deltaT, t0=h_plus.epoch)
        h_t_frequency = h_t.fft()
        asd_interp = asd.interpolate(float(np.array(h_t_frequency.df)))
        asd_interp = asd_interp[:len(h_t_frequency)]
        h_t_time = (h_t_frequency / asd_interp).ifft()
        h_t_time = h_t_time.highpass(30)
        h_t_time = h_t_time.lowpass(300)
        h_t_time.times = [float(np.array(i)) + ifo_time for i in h_t.times]

        strain_data_crop = strain_data_time.crop(ifo_time - 0.1, ifo_time + 0.06)
        try:
            h_t_time = h_t_time.crop(ifo_time - 0.1, ifo_time + 0.06)
        except Exception:
            pass
        max_strain = np.max(strain_data_crop).value

        plt.subplot(len(strain.keys()), 1, num + 1)
        plt.plot(strain_data_crop, color='grey', alpha=0.75, label="data")
        plt.plot(h_t_time, color='orange', label="template")
        plt.xlim([ifo_time - 0.1, ifo_time + 0.06])
        if not math.isnan(max_strain):
            plt.ylim([-max_strain * 1.5, max_strain * 1.5])
        plt.ylabel("Whitened %s strain" % (key), fontsize=8)
        plt.grid(False)
        plt.legend(loc="best", prop={'size': 8})
    plt.xlabel("Time $[s]$", fontsize=16)
    plt.tight_layout()
    return fig


def _format_prob(prob):
    """Format the probabilities for use with _classification_plot
    """
    if prob >= 1:
        return '100%'
    elif prob <= 0:
        return '0%'
    elif prob > 0.99:
        return '>99%'
    elif prob < 0.01:
        return '<1%'
    else:
        return '{}%'.format(int(np.round(100 * prob)))


def _classification_plot(classification):
    """Generate a bar chart showing the source classifications probabilities

    Parameters
    ----------
    classification: dict
        dictionary of source classifications
    """
    probs, names = zip(
        *sorted(zip(classification.values(), classification.keys())))
    with plt.style.context('seaborn-white'):
        fig, ax = plt.subplots(figsize=(2.5, 2))
        ax.barh(names, probs)
        for i, prob in enumerate(probs):
            ax.annotate(_format_prob(prob), (0, i), (4, 0),
                        textcoords='offset points', ha='left', va='center')
        ax.set_xlim(0, 1)
        ax.set_xticks([])
        ax.tick_params(left=False)
        for side in ['top', 'bottom', 'right']:
            ax.spines[side].set_visible(False)
        fig.tight_layout()
    return fig
