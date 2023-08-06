# Copyright (C) 2019 Charlie Hoy <charlie.hoy@ligo.org>
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

import os
import uuid
import numpy as np

import pesummary
from pesummary.core.webpage import webpage
from pesummary.core.webpage.main import _WebpageGeneration as _CoreWebpageGeneration
from pesummary.core.webpage.main import PlotCaption
from pesummary.gw.file.standard_names import descriptive_names
from pesummary.utils.utils import logger
from pesummary import conf


class CommandLineCaption(object):
    """Class to handle generating the command line used to generate a plot and
    a caption to describe the plot

    Parameters
    ----------
    """
    def __init__(self, command_line_arguments, samples=None):
        self.args = command_line_arguments
        self.samples = samples
        self.executable = self.get_executable("summaryplots")

    @staticmethod
    def get_executable(executable):
        """Return the path to an executable

        Parameters
        ----------
        executable: str
            the name of the executable you wish to find
        """
        from subprocess import check_output

        path = check_output(["which", executable]).decode("utf-8").strip()
        return path

    @property
    def command_line(self):
        """Generate the command line used to generate the plot
        """
        return "{} {}".format(self.executable, " ".join(self.args))

    @property
    def caption(self):
        """Make a caption to describe the plot
        """
        general_cli = ""
        if "1d_histogram" in self.args[0]:
            return self.histogram_caption()
        if "skymap" in self.args[0]:
            return self.skymap_caption()
        return general_cli

    def histogram_caption(self):
        """Return a caption to describe the 1d histogram plot
        """
        args = self.args[0].split(" ")
        parameter = args[args.index("--parameter") + 1]
        general_cli = (
            "1d histogram showing the posterior distribution for "
            "{}.".format(parameter)
        )
        if parameter == "chi_p":
            general_cli += (
                " chi_p is the precession parameter and quantifies how much "
                "precession there is in the system. It ranges from 0 to 1 "
                "with 0 meaning there is no precession in the system and 1 "
                "meaning there is maximal precession in the system."
            )
        if self.samples is not None:
            general_cli += (
                " The median of the distribution is {} with 90% confidence "
                "interval {}".format(
                    np.round(self.samples.average(type="median"), 3),
                    [np.round(i, 3) for i in self.samples.confidence_interval()]
                )
            )
        return general_cli

    def skymap_caption(self):
        """Return a caption to describe the skymap plot
        """
        general_cli = (
            "Skymap showing the possible location of the source of the "
            "source of the gravitational waves"
        )


class _WebpageGeneration(_CoreWebpageGeneration):
    """
    """
    def __init__(
        self, webdir=None, samples=None, labels=None, publication=None,
        user=None, config=None, same_parameters=None, base_url=None,
        file_versions=None, hdf5=None, colors=None, custom_plotting=None,
        pepredicates_probs=None, gracedb=None, approximant=None, key_data=None,
        file_kwargs=None, existing_labels=None, existing_config=None,
        existing_file_version=None, existing_injection_data=None,
        existing_samples=None, existing_metafile=None, add_to_existing=False,
        existing_file_kwargs=None, existing_weights=None, result_files=None,
        notes=None, disable_comparison=False, pastro_probs=None, gwdata=None,
        disable_interactive=False, publication_kwargs={}, no_ligo_skymap=False,
        psd=None, priors=None, package_information={"packages": []}
    ):
        self.pepredicates_probs = pepredicates_probs
        self.pastro_probs = pastro_probs
        self.gracedb = gracedb
        self.approximant = approximant
        self.key_data = key_data
        self.file_kwargs = file_kwargs
        self.publication = publication
        self.publication_kwargs = publication_kwargs
        self.result_files = result_files
        self.gwdata = gwdata
        self.no_ligo_skymap = no_ligo_skymap
        self.psd = psd
        self.priors = priors

        super(_WebpageGeneration, self).__init__(
            webdir=webdir, samples=samples, labels=labels,
            publication=publication, user=user, config=config,
            same_parameters=same_parameters, base_url=base_url,
            file_versions=file_versions, hdf5=hdf5, colors=colors,
            custom_plotting=custom_plotting,
            existing_labels=existing_labels, existing_config=existing_config,
            existing_file_version=existing_file_version,
            existing_injection_data=existing_injection_data,
            existing_samples=existing_samples,
            existing_metafile=existing_metafile,
            existing_file_kwargs=existing_file_kwargs,
            existing_weights=existing_weights,
            add_to_existing=add_to_existing, notes=notes,
            disable_comparison=disable_comparison,
            disable_interactive=disable_interactive,
            package_information=package_information
        )
        self.psd_path = {"other": os.path.join("..", "psds")}
        self.calibration_path = {"other": os.path.join("..", "calibration")}

    def categorize_parameters(self, parameters):
        """Categorize the parameters into common headings

        Parameters
        ----------
        parameters: list
            list of parameters that you would like to sort
        """
        params = []
        for heading, category in self.categories.items():
            if any(
                any(j in i for j in category["accept"]) for i in parameters
            ):
                cond = self._condition(category["accept"], category["reject"])
                params.append(
                    [heading, self._partition(cond, parameters)]
                )
        used_headings = [i[0] for i in params]
        other_index = \
            used_headings.index("others") if "others" in used_headings else None
        other_params = []
        for pp in parameters:
            if not any(pp in j[1] for j in params):
                if other_index is not None:
                    params[other_index][1].append(pp)
                else:
                    other_params.append(pp)
        if other_index is None:
            params.append(["others", other_params])
        return params

    def make_navbar_for_homepage(self):
        """Make a navbar for the homepage
        """
        links = [
            "home", ["Result Pages", self._result_page_links()], "Logging",
            "Version"
        ]
        if len(self.samples) > 1:
            links[1][1] += ["Comparison"]
        if self.publication:
            links.insert(2, "Publication")
        if self.gwdata is not None:
            links.append(["Detchar", [i for i in self.gwdata.keys()]])
        if self.notes is not None:
            links.append("Notes")
        return links

    def make_navbar_for_result_page(self):
        """Make a navbar for the result page homepage
        """
        links = {
            i: ["1d Histograms", [{"Custom": i}, {"All": i}]] for i in self.labels
        }
        for num, label in enumerate(self.labels):
            for j in self.categorize_parameters(self.samples[label].keys()):
                j = [j[0], [{k: label} for k in j[1]]]
                links[label].append(j)

        final_links = {
            i: [
                "home", ["Result Pages", self._result_page_links()],
                {"Corner": i}, {"Config": i}, links[i]
            ] for i in self.labels
        }
        if len(self.samples) > 1:
            for i in self.labels:
                final_links[i][1][1] += ["Comparison"]
        for num, label in enumerate(self.labels):
            if self.pepredicates_probs[label] is not None:
                final_links[label].append({"Classification": label})
        if self.make_interactive:
            for label in self.labels:
                final_links[label].append(
                    ["Interactive", [{"Interactive_Corner": label}]]
                )
        return final_links

    def generate_webpages(self):
        """Generate all webpages for all result files passed
        """
        if self.add_to_existing:
            self.add_existing_data()
        self.make_home_pages()
        self.make_1d_histogram_pages()
        self.make_corner_pages()
        self.make_config_pages()
        if self.make_comparison:
            self.make_comparison_pages()
        if self.make_interactive:
            self.make_interactive_pages()
        if self.publication:
            self.make_publication_pages()
        if self.gwdata is not None:
            self.make_detector_pages()
        if all(val is not None for key, val in self.pepredicates_probs.items()):
            self.make_classification_pages()
        self.make_error_page()
        self.make_version_page()
        self.make_logging_page()
        if self.notes is not None:
            self.make_notes_page()
        self.make_downloads_page()
        self.make_about_page()
        self.generate_specific_javascript()

    def _make_home_pages(self, pages):
        """Make the home pages

        Parameters
        ----------
        pages: list
            list of pages that you wish to create
        """
        title = None if self.gracedb is None else (
            "Parameter Estimation Summary Pages for {}".format(self.gracedb)
        )
        banner = "Summary" if self.gracedb is None else (
            "Summary for {}".format(self.gracedb)
        )
        html_file = self.setup_page("home", self.navbar["home"], title=title)
        html_file.make_banner(approximant=banner, key="Summary")
        path = self.image_path["home"]

        if self.make_comparison:
            if not all(self.approximant[i] is not None for i in self.labels):
                image_contents = []
                image_contents.append(
                    os.path.join(path, "compare_time_domain_waveforms.png")
                )
                image_contents = [image_contents]
                unique_id = '{}'.format(uuid.uuid4().hex.upper()[:6])
                html_file.make_table_of_images(
                    contents=image_contents, unique_id=unique_id
                )
                images = [y for x in image_contents for y in x]
                html_file.make_modal_carousel(images=images, unique_id=unique_id)

        for i in self.labels:
            html_file.make_banner(approximant=i, key=i)
            image_contents, captions = [], []
            basic_string = os.path.join(self.webdir, "plots", "{}.png")
            relative_path = os.path.join(path, "{}.png")
            if os.path.isfile(basic_string.format("%s_strain" % (i))):
                image_contents.append(relative_path.format("%s_strain" % (i)))
                captions.append(PlotCaption("strain"))
            if os.path.isfile(basic_string.format("%s_psd_plot" % (i))):
                image_contents.append(relative_path.format("%s_psd_plot" % (i)))
                captions.append(PlotCaption("psd"))
            if os.path.isfile(
                basic_string.format("%s_waveform_time_domain" % (i))
            ):
                image_contents.append(
                    relative_path.format("%s_waveform_time_domain" % (i))
                )
                captions.append(PlotCaption("time_waveform"))
            if os.path.isfile(
                basic_string.format("%s_calibration_plot" % (i))
            ):
                image_contents.append(
                    relative_path.format("%s_calibration_plot" % (i))
                )
                captions.append(PlotCaption("calibration"))
            image_contents = [image_contents]
            unique_id = '{}'.format(uuid.uuid4().hex.upper()[:6])
            html_file.make_table_of_images(
                contents=image_contents, unique_id=unique_id,
                captions=[captions], extra_div=True
            )
            images = [y for x in image_contents for y in x]
            html_file.make_modal_carousel(images=images, unique_id=unique_id)
            if self.file_kwargs[i]["sampler"] != {}:
                html_file.make_banner(
                    approximant="Sampler kwargs", key="sampler_kwargs",
                    _style="font-size: 26px;"
                )
                _style = "margin-top:3em; margin-bottom:5em;"
                html_file.make_container(style=_style)
                _class = "row justify-content-center"
                html_file.make_div(4, _class=_class, _style=None)
                keys = list(self.file_kwargs[i]["sampler"].keys())
                table_contents = [
                    [self.file_kwargs[i]["sampler"][key] for key in keys]
                ]
                html_file.make_table(
                    headings=keys, format="table-hover", contents=table_contents,
                    heading_span=1, accordian=False
                )
                html_file.end_div(4)
                html_file.end_container()
            if self.file_kwargs[i]["meta_data"] != {}:
                html_file.make_banner(
                    approximant="Meta data", key="meta_data",
                    _style="font-size: 26px; margin-top: -3em"
                )
                _style = "margin-top:3em; margin-bottom:5em;"
                html_file.make_container(style=_style)
                _class = "row justify-content-center"
                html_file.make_div(4, _class=_class, _style=None)
                keys = list(self.file_kwargs[i]["meta_data"].keys())
                table_contents = [
                    [self.file_kwargs[i]["meta_data"][key] for key in keys]
                ]
                html_file.make_table(
                    headings=keys, format="table-hover", contents=table_contents,
                    heading_span=1, accordian=False
                )
                html_file.end_div(4)
                html_file.end_container()
        html_file.make_footer(user=self.user, rundir=self.webdir)
        html_file.close()

        for num, i in enumerate(self.labels):
            html_file = self.setup_page(
                i, self.navbar["result_page"][i], i, approximant=i,
                title="{} Summary page".format(i),
                background_colour=self.colors[num]
            )
            html_file.make_banner(approximant=i, key=i)
            images, cli, captions = self.default_images_for_result_page(i)
            unique_id = '{}'.format(uuid.uuid4().hex.upper()[:6])
            html_file.make_table_of_images(
                contents=images, cli=cli, unique_id=unique_id,
                captions=captions
            )
            images = [y for x in images for y in x]
            html_file.make_modal_carousel(images=images, unique_id=unique_id)

            if self.custom_plotting:
                from glob import glob

                custom_plots = glob(
                    "{}/plots/{}_custom_plotting_*".format(self.webdir, i)
                )
                path = self.image_path["other"]
                for num, i in enumerate(custom_plots):
                    custom_plots[num] = path + i.split("/")[-1]
                image_contents = [
                    custom_plots[i:4 + i] for i in range(
                        0, len(custom_plots), 4
                    )
                ]
                unique_id = '{}'.format(uuid.uuid4().hex.upper()[:6])
                html_file.make_table_of_images(
                    contents=image_contents, unique_id=unique_id
                )
                images = [y for x in image_contents for y in x]
                html_file.make_modal_carousel(images=images, unique_id=unique_id)

            key_data = self.key_data
            contents = []
            for j in self.samples[i].keys():
                row = []
                row.append(j)
                row.append(np.round(self.key_data[i][j]["maxL"], 3))
                row.append(np.round(self.key_data[i][j]["mean"], 3))
                row.append(np.round(self.key_data[i][j]["median"], 3))
                row.append(np.round(self.key_data[i][j]["std"], 3))
                contents.append(row)

            html_file.make_table(
                headings=[" ", "maxL", "mean", "median", "std"],
                contents=contents, heading_span=1
            )
            html_file.export(
                "summary_information_{}.csv".format(i)
            )
            html_file.make_footer(user=self.user, rundir=self.webdir)
            html_file.close()

    def _make_corner_pages(self, pages):
        """Make the corner pages

        Parameters
        ----------
        pages: list
            list of pages that you wish to create
        """
        for num, i in enumerate(self.labels):
            html_file = self.setup_page(
                "{}_Corner".format(i), self.navbar["result_page"][i], i,
                title="{} Corner Plots".format(i), approximant=i,
                background_colour=self.colors[num]
            )
            html_file.make_banner(approximant=i, key="corner")
            params = [
                "luminosity_distance", "dec", "a_2", "phase",
                "a_1", "geocent_time", "phi_jl", "psi", "ra",
                "mass_2", "mass_1", "phi_12", "tilt_2", "iota",
                "tilt_1", "chi_p", "chirp_mass", "mass_ratio",
                "symmetric_mass_ratio", "total_mass", "chi_eff",
                "redshift", "mass_1_source", "mass_2_source",
                "total_mass_source", "chirp_mass_source",
                "lambda_1", "lambda_2", "delta_lambda",
                "lambda_tilde"
            ]
            included_parameters = [
                i for i in list(self.samples[i].keys()) if i in params
            ]
            html_file.make_search_bar(
                sidebar=included_parameters,
                popular_options=self.popular_options + [{
                    "all": ", ".join(included_parameters)
                }], label=i
            )
            html_file.make_footer(user=self.user, rundir=self.webdir)
            html_file.close()

    def _make_comparison_pages(self, pages):
        """Make the comparison pages

        Parameters
        ----------
        pages: list
            list of pages that you wish to create
        """
        html_file = self.setup_page(
            "Comparison", self.navbar["comparison"],
            title="Comparison Summary Page", approximant="Comparison"
        )
        html_file.make_banner(approximant="Comparison", key="Comparison")
        path = self.image_path["other"]
        base = os.path.join(path, "{}.png")
        contents = [
            [base.format("combined_skymap"), base.format("compare_waveforms")]
        ]
        unique_id = '{}'.format(uuid.uuid4().hex.upper()[:6])
        html_file.make_table_of_images(contents=contents, unique_id=unique_id)
        images = [y for x in contents for y in x]
        html_file.make_modal_carousel(images=images, unique_id=unique_id)
        if self.custom_plotting:
            from glob import glob

            custom_plots = glob(
                os.path.join(
                    self.webdir, "plots", "combined_custom_plotting_*"
                )
            )
            for num, i in enumerate(custom_plots):
                custom_plots[num] = path + i.split("/")[-1]
            image_contents = [
                custom_plots[i:4 + i] for i in range(0, len(custom_plots), 4)
            ]
            unique_id = '{}'.format(uuid.uuid4().hex.upper()[:6])
            html_file.make_table_of_images(
                contents=image_contents, unique_id=unique_id
            )
            images = [y for x in image_contents for y in x]
            html_file.make_modal_carousel(images=images, unique_id=unique_id)

        if self.comparison_stats is not None:
            rows = range(len(self.labels))
            base = (
                "margin-top:{}em; margin-bottom:{}em; background-color:#FFFFFF; "
                "box-shadow: 0 0 5px grey;"
            )
            style_ks = base.format(5, 1)
            style_js = base.format(0, 5)

            table_contents = {
                i: [
                    [self.labels[j]] + self.comparison_stats[i][0][j] for j in
                    rows
                ] for i in self.same_parameters
            }
            html_file.make_table(
                headings=[" "] + self.labels, contents=table_contents,
                heading_span=1, accordian_header="KS test total", style=style_ks
            )
            table_contents = {
                i: [
                    [self.labels[j]] + self.comparison_stats[i][1][j] for j in
                    rows
                ] for i in self.same_parameters
            }
            html_file.make_table(
                headings=[" "] + self.labels, contents=table_contents,
                heading_span=1, accordian_header="JS test total", style=style_js
            )
        html_file.make_footer(user=self.user, rundir=self.webdir)

        for num, i in enumerate(self.same_parameters):
            html_file = self.setup_page(
                "Comparison_{}".format(i), self.navbar["comparison"],
                title="Comparison PDF for {}".format(i),
                approximant="Comparison"
            )
            html_file.make_banner(approximant="Comparison", key="Comparison")
            path = self.image_path["other"]
            contents = [
                [path + "combined_1d_posterior_{}.png".format(i)],
                [
                    path + "combined_cdf_{}.png".format(i),
                    path + "combined_boxplot_{}.png".format(i)
                ]
            ]
            html_file.make_table_of_images(
                contents=contents, rows=1, columns=2, code="changeimage"
            )
            if self.comparison_stats is not None:
                table_contents = [
                    [self.labels[j]] + self.comparison_stats[i][0][j]
                    for j in rows
                ]
                html_file.make_table(
                    headings=[" "] + self.labels, contents=table_contents,
                    heading_span=1, accordian_header="KS test",
                    style=style_ks
                )
                table_contents = [
                    [self.labels[j]] + self.comparison_stats[i][1][j]
                    for j in rows
                ]
                html_file.make_table(
                    headings=[" "] + self.labels, contents=table_contents,
                    heading_span=1, accordian_header="JS divergence test",
                    style=style_js
                )
            html_file.make_footer(user=self.user, rundir=self.webdir)
            html_file.close()
        html_file = self.setup_page(
            "Comparison_Custom", self.navbar["comparison"],
            approximant="Comparison", title="Comparison Posteriors for multiple"
        )
        html_file.make_search_bar(
            sidebar=self.same_parameters, label="None", code="combines",
            popular_options=self.popular_options + [{
                "all": ", ".join(self.same_parameters)
            }]
        )
        html_file.make_footer(user=self.user, rundir=self.webdir)
        html_file.close()
        html_file = self.setup_page(
            "Comparison_All", self.navbar["comparison"],
            title="All posteriors for Comparison", approximant="Comparison"
        )
        html_file.make_banner(approximant="Comparison", key="Comparison")
        for j in self.same_parameters:
            html_file.make_banner(
                approximant=j, _style="font-size: 26px;"
            )
            contents = [
                [path + "combined_1d_posterior_{}.png".format(j)],
                [
                    path + "combined_cdf_{}.png".format(j),
                    path + "combined_boxplot_{}.png".format(j)
                ]
            ]
            html_file.make_table_of_images(
                contents=contents, rows=1, columns=2, code="changeimage")
        html_file.close()

    def make_publication_pages(self):
        """Wrapper function for _make_publication_pages()
        """
        pages = ["Publication"]
        self.create_blank_html_pages(pages)
        self._make_publication_pages(pages)

    def _make_publication_pages(self, pages):
        """Make the publication pages

        Parameters
        ----------
        pages: list
            list of pages that you wish to create
        """
        from glob import glob

        executable = self.get_executable("summarypublication")
        general_cli = "%s --webdir %s --samples %s --labels %s --plot {}" % (
            executable, os.path.join(self.webdir, "plots", "publication"),
            " ".join(self.result_files), " ".join(self.labels)
        )
        if self.publication_kwargs != {}:
            general_cli += "--publication_kwargs %s" % (
                " ".join(
                    [
                        "{}:{}".format(key, value) for key, value in
                        self.publication_kwargs.items()
                    ]
                )
            )
        html_file = self.setup_page(
            "Publication", self.navbar["home"], title="Publication Plots"
        )
        html_file.make_banner(approximant="Publication", key="Publication")
        path = self.image_path["other"]
        pub_plots = glob(
            os.path.join(self.webdir, "plots", "publication", "*.png")
        )
        for num, i in enumerate(pub_plots):
            shortened_path = i.split("/plots/")[-1]
            pub_plots[num] = path + shortened_path
        cli = []
        cap = []
        posterior_name = \
            lambda i: "{} ({})".format(i, descriptive_names[i]) if i in \
            descriptive_names.keys() and descriptive_names[i] != "" else i
        for i in pub_plots:
            filename = i.split("/")[-1]
            if "violin_plot" in filename:
                parameter = filename.split("violin_plot_")[-1].split(".png")[0]
                cli.append(
                    general_cli.format("violin") + " --parameters %s" % (
                        parameter
                    )
                )
                cap.append(
                    PlotCaption("violin").format(posterior_name(parameter))
                )
            elif "spin_disk" in filename:
                cli.append(general_cli.format("spin_disk"))
                cap.append(PlotCaption("spin_disk"))
            elif "2d_contour" in filename:
                parameters = filename.split("2d_contour_plot_")[-1].split(".png")[0]
                cli.append(
                    general_cli.format("2d_contour") + " --parameters %s" % (
                        parameters.replace("_and_", " ")
                    )
                )
                pp = parameters.split("_and_")
                cap.append(
                    PlotCaption("2d_contour").format(
                        posterior_name(pp[0]), posterior_name(pp[1])
                    )
                )
        image_contents = [
            pub_plots[i:3 + i] for i in range(0, len(pub_plots), 3)
        ]
        command_lines = [
            cli[i:3 + i] for i in range(0, len(cli), 3)
        ]
        captions = [cap[i:3 + i] for i in range(0, len(cap), 3)]
        html_file.make_table_of_images(
            contents=image_contents, cli=command_lines, captions=captions
        )
        images = [y for x in image_contents for y in x]
        html_file.make_modal_carousel(images=images)
        html_file.make_footer(user=self.user, rundir=self.webdir)
        html_file.close()

    def make_detector_pages(self):
        """Wrapper function for _make_publication_pages()
        """
        pages = [i for i in self.gwdata.keys()]
        self.create_blank_html_pages(pages)
        self._make_detector_pages(pages)

    def _make_detector_pages(self, pages):
        """Make the detector characterisation pages

        Parameters
        ----------
        pages: list
            list of pages that you wish to create
        """
        from glob import glob
        from pesummary.utils.utils import (
            determine_gps_time_and_window, command_line_dict
        )
        from astropy.time import Time

        executable = self.get_executable("summarydetchar")
        command_line = command_line_dict()
        if isinstance(command_line["gwdata"], dict):
            gwdata_command_line = [
                "{}:{}".format(key, val) for key, val in
                command_line["gwdata"].items()
            ]
        else:
            gwdata_command_line = command_line["gwdata"]
        general_cli = "%s --webdir %s --gwdata %s --plot {}{}" % (
            executable, os.path.join(self.webdir, "plots"),
            " ".join(gwdata_command_line)
        )
        path = self.image_path["other"]
        base = os.path.join(path, "{}_{}.png")
        maxL_samples = {
            i: {
                "geocent_time": self.key_data[i]["geocent_time"]["maxL"]
            } for i in self.labels
        }
        gps_time, window = determine_gps_time_and_window(maxL_samples, self.labels)
        t = Time(gps_time, format='gps')
        t = Time(t, format='datetime')
        link = (
            "https://ldas-jobs.ligo-wa.caltech.edu/~detchar/summary/day"
            "/{}{}{}/".format(
                t.value.year,
                "0{}".format(t.value.month) if t.value.month < 10 else t.value.month,
                "0{}".format(t.value.day) if t.value.day < 10 else t.value.day
            )
        )
        for det in self.gwdata.keys():
            html_file = self.setup_page(
                det, self.navbar["home"], title="{} Detchar".format(det)
            )
            html_file.make_banner(approximant=det, key="detchar", link=link)
            image_contents = [
                [base.format("spectrogram", det), base.format("omegascan", det)]
            ]
            command_lines = [
                [
                    general_cli.format("spectrogram", ""),
                    general_cli.format(
                        "omegascan", "--gps %s --vmin 0 --vmax 25 --window %s" % (
                            gps_time, window
                        )
                    )
                ]
            ]
            html_file.make_table_of_images(
                contents=image_contents, cli=command_lines, autoscale=True
            )
            images = [y for x in image_contents for y in x]
            html_file.make_modal_carousel(images=images)
            html_file.make_footer(user=self.user, rundir=self.webdir)
            html_file.close()

    def make_classification_pages(self):
        """Wrapper function for _make_publication_pages()
        """
        pages = ["{}_{}_Classification".format(i, i) for i in self.labels]
        self.create_blank_html_pages(pages)
        self._make_classification_pages(pages)

    def _make_classification_pages(self, pages):
        """Make the classification pages

        Parameters
        ----------
        pages: list
            list of pages that you wish to create
        """
        executable = self.get_executable("summaryclassification")
        general_cli = "%s --samples {}" % (executable)
        for num, label in enumerate(self.labels):
            html_file = self.setup_page(
                "{}_Classification".format(label),
                self.navbar["result_page"][label], label,
                title="{} Classification".format(label),
                background_colour=self.colors[num], approximant=label
            )
            html_file.make_banner(approximant=label, key="classification")

            if self.pepredicates_probs[label] is not None:
                html_file.make_container()
                _class = "row justify-content-center"
                html_file.make_div(4, _class=_class, _style=None)
                keys = list(self.pepredicates_probs[label]["default"].keys())
                table_contents = [
                    ["{} prior".format(i)] + [
                        self.pepredicates_probs[label][i][j] for j in keys
                    ] for i in ["default", "population"]
                ]
                if self.pastro_probs[label] is not None:
                    keys += ["HasNS"]
                    keys += ["HasRemnant"]
                    table_contents[0].append(self.pastro_probs[label]["default"]["HasNS"])
                    table_contents[0].append(
                        self.pastro_probs[label]["default"]["HasRemnant"]
                    )
                    try:
                        table_contents[1].append(
                            self.pastro_probs[label]["population"]["HasNS"]
                        )
                        table_contents[1].append(
                            self.pastro_probs[label]["population"]["HasRemnant"]
                        )
                    except KeyError:
                        table_contents[1].append("-")
                        table_contents[1].append("-")
                        logger.warn(
                            "Failed to add 'em_bright' probabilities for population "
                            "reweighted prior"
                        )
                html_file.make_table(
                    headings=[" "] + keys, contents=table_contents,
                    heading_span=1, accordian=False
                )
                html_file.make_cli_button(
                    general_cli.format(self.result_files[num])
                )
                html_file.export(
                    "classification_{}.csv".format(label),
                    margin_top="-1.5em", margin_bottom="0.5em", json=True
                )
                html_file.end_div(4)
                html_file.end_container()
            path = self.image_path["other"]
            base = os.path.join(path, "%s_{}_pepredicates{}.png" % (label))
            image_contents = [
                [
                    base.format("default", ""), base.format("default", "_bar"),
                    base.format("population", ""),
                    base.format("population", "_bar")
                ]
            ]
            base = (
                "%s --webdir %s --labels %s --plot {} --prior {}" % (
                    general_cli.format(self.result_files[num]),
                    os.path.join(self.webdir, "plots"), label
                )
            )
            command_lines = [
                [
                    base.format("mass_1_mass_2", "default"),
                    base.format("bar", "default"),
                    base.format("mass_1_mass_2", "population"),
                    base.format("bar", "population")
                ]
            ]
            captions = [
                [
                    PlotCaption("default_classification_mass_1_mass_2"),
                    PlotCaption("default_classification_bar"),
                    PlotCaption("population_classification_mass_1_mass_2"),
                    PlotCaption("population_classification_bar")
                ]
            ]
            html_file.make_table_of_images(
                contents=image_contents, cli=command_lines, autoscale=True,
                captions=captions
            )
            images = [y for x in image_contents for y in x]
            html_file.make_modal_carousel(images=images)
            html_file.make_footer(user=self.user, rundir=self.webdir)
            html_file.close()

    def _make_downloads_page(self, pages):
        """Make a page with links to files which can be downloaded

        Parameters
        ----------
        pages: list
            list of pages you wish to create
        """
        html_file = webpage.open_html(
            web_dir=self.webdir, base_url=self.base_url, html_page="Downloads"
        )
        html_file = self.setup_page(
            "Downloads", self.navbar["home"], title="Downloads"
        )
        html_file.make_banner(approximant="Downloads", key="Downloads")
        html_file.make_container()
        base_string = "{} can be downloaded <a href={} download>here</a>"
        style = "margin-top:{}; margin-bottom:{};"
        headings = ["Description"]
        metafile = (
            "posterior_samples.json" if not self.hdf5 else "posterior_samples.h5"
        )
        html_file.make_table(
            headings=headings,
            contents=[
                [
                    base_string.format(
                        "The complete metafile containing all information "
                        "about the analysis",
                        self.results_path["other"] + metafile
                    )
                ], [
                    (
                        "Information about reading this metafile can be seen "
                        " <a href={}>here</a>".format(
                            "https://lscsoft.docs.ligo.org/pesummary/data/"
                            "reading_the_metafile.html"
                        )
                    )
                ]
            ],
            accordian=False, style=style.format("1em", "1em")
        )
        for num, i in enumerate(self.labels):
            html_file.add_content(
                "<div class='banner', style='margin-left:-4em'>{}</div>".format(i)
            )
            table_contents = [
                [
                    base_string.format(
                        "Dat file containing posterior samples",
                        self.results_path["other"] + "%s_pesummary.dat" % (i)
                    )
                ]
            ]
            if self.config is not None and self.config[num] is not None:
                table_contents.append(
                    [
                        base_string.format(
                            "Config file used for this analysis",
                            self.config_path["other"] + "%s_config.ini" % (i)
                        )
                    ]
                )
            if not self.no_ligo_skymap:
                table_contents.append(
                    [
                        base_string.format(
                            "Fits file containing skymap for this analysis",
                            self.results_path["other"] + "%s_skymap.fits" % (i)
                        )
                    ]
                )
            if self.psd is not None and self.psd != {} and i in self.psd.keys():
                for ifo in self.psd[i].keys():
                    if len(self.psd[i][ifo]):
                        table_contents.append(
                            [
                                base_string.format(
                                    "%s psd file used for this analysis" % (ifo),
                                    os.path.join(
                                        self.psd_path["other"],
                                        "%s_%s_psd.dat" % (i, ifo)
                                    )
                                )
                            ]
                        )
            if "calibration" in self.priors.keys():
                if i in self.priors["calibration"].keys():
                    for ifo in self.priors["calibration"][i].keys():
                        table_contents.append(
                            [
                                base_string.format(
                                    "%s calibration envelope file used for this "
                                    "analysis" % (ifo), os.path.join(
                                        self.calibration_path["other"],
                                        "%s_%s_cal.txt" % (i, ifo)
                                    )
                                )
                            ]
                        )
            html_file.make_table(
                headings=headings, contents=table_contents, accordian=False
            )
        html_file.end_container()
        html_file.make_footer(user=self.user, rundir=self.webdir)
        html_file.close()

    def default_images_for_result_page(self, label):
        """Return the default images that will be displayed on the result page
        """
        path = self.image_path["other"]
        base_string = path + "%s_{}.png" % (label)
        image_contents = [
            [
                base_string.format("1d_posterior_mass_1"),
                base_string.format("1d_posterior_mass_2"),
                base_string.format("1d_posterior_a_1"),
            ], [
                base_string.format("1d_posterior_a_2"),
                base_string.format("skymap"),
                base_string.format("waveform"),
            ], [
                base_string.format("1d_posterior_iota"),
                base_string.format("1d_posterior_luminosity_distance"),
                base_string.format("1d_posterior_chi_eff")
            ]
        ]
        executable = self.get_executable("summaryplots")
        general_cli = (
            "%s --webdir %s --samples %s --burnin %s --plot {} {} "
            "--labels %s" % (
                executable, os.path.join(self.webdir, "plots"),
                self.result_files[self.labels.index(label)], conf.burnin, label
            )
        )
        cli = [
            [
                general_cli.format("1d_histogram", "--parameter mass_1"),
                general_cli.format("1d_histgram", "--parameter mass_2"),
                general_cli.format("1d_histogram", "--parameter a_1"),
            ], [
                general_cli.format("1d_histogram", "--parameter a_2"),
                general_cli.format("skymap", ""),
                general_cli.format("waveform", ""),
            ], [
                general_cli.format("1d_histogram", "--parameter iota"),
                general_cli.format(
                    "1d_histogram", "--parameter luminosity_distance"
                ),
                general_cli.format("1d_histogram", "--parameter chi_eff")
            ]
        ]

        caption_1d_histogram = PlotCaption("1d_histogram")
        posterior_name = \
            lambda i: "{} ({})".format(i, descriptive_names[i]) if i in \
            descriptive_names.keys() and descriptive_names[i] != "" else i
        captions = [
            [
                caption_1d_histogram.format(posterior_name("mass_1")),
                caption_1d_histogram.format(posterior_name("mass_2")),
                caption_1d_histogram.format(posterior_name("a_1")),
            ], [
                caption_1d_histogram.format(posterior_name("a_2")),
                PlotCaption("skymap"), PlotCaption("frequency_waveform"),
            ], [
                caption_1d_histogram.format(posterior_name("iota")),
                caption_1d_histogram.format(posterior_name("luminosity_distance")),
                caption_1d_histogram.format(posterior_name("chi_eff"))
            ]
        ]
        return image_contents, cli, captions

    def default_categories(self):
        """Return the default categories
        """
        categories = self.categories = {
            "masses": {
                "accept": ["mass"],
                "reject": ["source", "final"]
            },
            "source": {
                "accept": ["source"], "reject": ["final"]
            },
            "remnant": {
                "accept": ["final"], "reject": []
            },
            "inclination": {
                "accept": ["theta", "iota"], "reject": []
            },
            "spins": {
                "accept": ["spin", "chi_p", "chi_eff", "a_1", "a_2"],
                "reject": ["lambda", "final"]
            },
            "spin_angles": {
                "accept": ["phi", "tilt"], "reject": []
            },
            "tidal": {
                "accept": ["lambda"], "reject": []
            },
            "location": {
                "accept": [
                    "ra", "dec", "psi", "luminosity_distance", "redshift",
                    "comoving_distance"
                ],
                "reject": ["mass_ratio"]
            },
            "timings": {
                "accept": ["time"], "reject": []
            },
            "SNR": {
                "accept": ["snr"], "reject": []
            },
            "calibration": {
                "accept": ["spcal", "recalib", "frequency"],
                "reject": ["minimum"]
            },
            "energy": {
                "accept": ["peak_luminosity", "radiated"],
                "reject": []
            },
            "others": {
                "accept": ["phase", "likelihood", "prior"],
                "reject": ["spcal", "recalib"]
            }
        }
        return categories

    def default_popular_options(self):
        """Return a list of popular options
        """
        popular_options = [
            "mass_1, mass_2", "luminosity_distance, iota, ra, dec",
            "iota, phi_12, phi_jl, tilt_1, tilt_2"
        ]
        return popular_options
