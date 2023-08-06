"""
Created on 2019.08.15
:author: Felix Soubelet

A simply script to run analysis and get insight on my use of equipment and settings in my practice of photography.
"""

import argparse
import pathlib
from multiprocessing import Pool, cpu_count

import pandas as pd
import pyexifinfo as pyexif
from fsbox import logging_tools
from fsbox.contexts import timeit

from photocrawl.plotting_functions import plot_insight

LEVELS_DICT: dict = {
    "debug": logging_tools.DEBUG,
    "info": logging_tools.INFO,
    "warning": logging_tools.WARNING,
    "error": logging_tools.ERROR,
}
LOGGER = logging_tools.get_logger(__name__)


class PhotoCrawler:
    """
    Class to handle the crawling and processing of different files.
    """

    def __init__(self, directory_to_crawl: pathlib.Path):
        self.top_level_location: pathlib.Path = directory_to_crawl
        self.categorical_columns: list = [
            "Exposure_Compensation",
            "Exposure_Program",
            "Flash",
            "Lens_Brand",
            "Lens",
            "Brand",
            "Metering_Mode",
            "Camera",
            "Shutter_Speed",
            "White_Balance",
            "Focal_Range",
        ]
        self.columns_renaming_dict: dict = {
            "ExposureCompensation": "Exposure_Compensation",
            "ExposureProgram": "Exposure_Program",
            "FNumber": "F_Number",
            "FocalLengthIn35mmFormat": "Focal_Length",
            "LensMake": "Lens_Brand",
            "LensModel": "Lens",
            "Make": "Brand",
            "MeteringMode": "Metering_Mode",
            "Model": "Camera",
            "ShutterSpeedValue": "Shutter_Speed",
            "WhiteBalance": "White_Balance",
        }
        self.interesting_features: list = [
            "DateTimeOriginal",
            "ExposureCompensation",
            "ExposureProgram",
            "FNumber",
            "Flash",
            "FocalLengthIn35mmFormat",
            "ISO",
            "LensMake",
            "LensModel",
            "Make",
            "MeteringMode",
            "Model",
            "ShutterSpeedValue",
            "WhiteBalance",
        ]
        self.lens_tags_mapping: dict = {
            "XF10-24mmF4 R OIS": "XF 10-24mm f/4 R",
            "XF18-135mmF3.5-5.6R LM IOS WR": "XF 18-135mm f/3.5-5.6 R LM OIS WR",
            "XF18-55mmF2.8-4 R LM OIS": "XF 18-55mm f/2.8-4 R LM OIS",
            "XF23mmF1.4 R": "XF 23mm f/1.4 R",
            "XF50-140mmF2.8 R LM OIS WR": "XF 50-140mm f/2.8 R LM OIS WR",
            "XF50-140mmF2.8 R LM OIS WR + 1.4x": "XF 50-140mm f/2.8 R LM OIS WR + 1.4x",
            "XF55-200mmF3.5-4.8 R LM OIS": "XF 55-200mm f/3.5-4.8 R LM OIS",
            "XF56mmF1.2 R APD": "XF 56mm f/1.2 R APD",
        }
        self.metering_modes_mapping: dict = {
            "Center-weighted average": "Center Weighted",
            "Multi-segment": "Multi Segment",
        }
        self.raw_formats: dict = {
            "JPG": "The classic jpg file format",
            "JPEG": "Also the jpg file format",
            "3FR": "Hasselblad 3F RAW Image",
            "ARI": "ARRIRAW Image",
            "ARW": "Sony Digital Camera Image",
            "BAY": "Casio RAW Image",
            "CR2": "Canon Raw Image File",
            "CR3": "Canon Raw 3 Image File",
            "CRW": "Canon Raw CIFF Image File",
            "CS1": "CaptureShop 1-shot Raw Image",
            "CXI": "FMAT RAW Image",
            "DCR": "Kodak RAW Image File",
            "DNG": "Digital Negative Image File",
            "EIP": "Enhanced Image Package File",
            "ERF": "Epson RAW File",
            "FFF": "Hasselblad RAW Image",
            "IIQ": "Phase One RAW Image",
            "J6I": "Ricoh Camera Image File",
            "K25": "Kodak K25 Image",
            "KDC": "Kodak Photo-Enhancer File",
            "MEF": "Mamiya RAW Image",
            "MFW": "Mamiya Camera Raw File",
            "MOS": "Leaf Camera RAW File",
            "MRW": "Minolta Raw Image File",
            "NEF": "Nikon Electronic Format RAW Image",
            "NRW": "Nikon Raw Image File",
            "ORF": "Olympus RAW File",
            "PEF": "Pentax Electronic File",
            "RAF": "Fuji RAW Image File",
            "RAW": "Raw Image Data File",
            "RW2": "Panasonic RAW Image",
            "RWL": "Leica RAW Image",
            "RWZ": "Rawzor Compressed Image",
            "SR2": "Sony RAW Image",
            "SRF": "Sony RAW Image",
            "SRW": "Samsung RAW Image",
            "X3F": "SIGMA X3F Camera RAW File",
        }

    def get_exif(self, photo_file: str) -> dict:
        """
        Returns a dictionary with interesting features from image EXIF.

        Args:
            photo_file: A `pathlib.Path` object with the bsolute path to the file location.

        Returns:
            A dictionary with the exif fields and value for the specific file.
        """
        return {
            key[5:]: value
            for key, value in pyexif.get_json(photo_file)[0].items()
            if key[5:] in self.interesting_features
        }

    def process_files(self) -> pd.DataFrame:
        """
        Recursively go over relevant files in the `top_level_localtion` directory and sub-directories,
        and organize their exif data in a `pandas.DataFrame`.

        Returns:
            A `pandas.DataFrame` with exif information for each file. Each file's information is a row,
            and each column corresponds to an exif data field.
        """
        crawled_images: list = []
        with timeit(lambda spanned: LOGGER.info(f"Crawled and found all relevant files in {spanned:.4f} seconds.")):
            for extension in self.raw_formats.keys():
                crawled_images.extend(self.top_level_location.glob(f"**/*.{extension}"))
                crawled_images.extend(self.top_level_location.glob(f"**/*.{extension.lower()}"))
            crawled_images = sorted(str(result) for result in crawled_images)

        with timeit(
            lambda spanned: LOGGER.info(f"Processed metadata of {len(crawled_images)} files in {spanned:.4f} seconds.")
        ):
            with Pool(cpu_count()) as pool:
                metadata = pd.DataFrame(list(pool.imap_unordered(self.get_exif, crawled_images)))
        return metadata

    def refactor_exif_data(self, crawled_exif: pd.DataFrame) -> pd.DataFrame:
        """
        Refactor the `pandas.Dataframe` with crawled exif data by improving labels and categorizing some content
        from original.

        Returns:
            A new `pandas.DataFrame` with refactored data.
        """
        with timeit(lambda spanned: LOGGER.info(f"Refactorred metadata in {spanned:.4f} seconds")):
            working_df: pd.DataFrame = crawled_exif.copy(deep=True)
            working_df.rename(self.columns_renaming_dict, axis="columns", inplace=True)
            working_df.dropna(inplace=True)

            LOGGER.debug("Refactoring shots dates.")
            working_df["Year"] = working_df["DateTimeOriginal"].str[:4]
            working_df["Month"] = working_df["DateTimeOriginal"].str[5:7]
            working_df["Day"] = working_df["DateTimeOriginal"].str[8:10]

            LOGGER.debug("Extrapolating focal ranges.")
            working_df["Focal_Length"] = working_df["Focal_Length"].apply(lambda x: int(str(x[:3])))
            working_df["Focal_Range"] = working_df.apply(lambda row: _figure_focal_range(row), axis=1)

            LOGGER.debug("Making data categorical.")
            for column in self.categorical_columns:
                working_df[column] = working_df[column].astype("category")

            LOGGER.debug("Refactoring metering mode names")
            working_df["Metering_Mode"] = (
                working_df["Metering_Mode"].map(self.metering_modes_mapping).fillna(working_df["Metering_Mode"])
            )

            # Does the mapping, and falls back to original names for values absent in the mapping dictionary
            LOGGER.debug("Refactoring lens names. Might not be exhaustive.")
            working_df["Lens"] = working_df["Lens"].cat.remove_unused_categories()
            working_df["Lens"] = working_df["Lens"].map(self.lens_tags_mapping).fillna(working_df["Lens"])
        return working_df.dropna()


def crawl() -> None:
    """
    Gets location from commandline arguments, crawls relevant files and performs analysis.
    Will plot and save figures.

    Returns:
        Nothing.
    """
    _set_logger_level()
    output_directory: pathlib.Path = _setup_output_directory("example_outputs")
    files_location = pathlib.Path(_parse_args()[0])

    crawler = PhotoCrawler(files_location)
    exif_data_df = crawler.process_files()
    exif_data_df = crawler.refactor_exif_data(exif_data_df)

    plot_insight(exif_data_df, output_directory)


# ==================================================================================================================== #


def _figure_focal_range(row: pd.Series) -> str:
    """
    Categorize the focal length value in different ranges. This is better for plotting the number of shots per focal
    length (focal range). To be applied as a lambda on a column of your DataFrame.

    Args:
        row: a `pandas.Series` object with different focal lengths values as integers or floats.

    Returns:
        A String for each value, corresponding to the focal range,
    """
    if row["Focal_Length"] < 10:
        return "1-9mm"
    if 10 <= row["Focal_Length"] < 16:
        return "10-15mm"
    if 16 <= row["Focal_Length"] < 23:
        return "16-23mm"
    if 24 <= row["Focal_Length"] < 70:
        return "24-70mm"
    if 70 <= row["Focal_Length"] < 200:
        return "70-200mm"
    if 200 <= row["Focal_Length"] < 400:
        return "200-400mm"
    if row["Focal_Length"] > 400:
        return "400mm+"


def _parse_args() -> tuple:
    """
    Simple argument parser to make life easier in the command-line.
    """
    parser = argparse.ArgumentParser(description="Running MAD-X AC dipole trackings for you.")
    parser.add_argument(
        "-i",
        "--images",
        dest="location",
        default=None,
        type=str,
        help="Location, either relative or absolute, of the directory in which are images you wish to crawl",
    )
    parser.add_argument(
        "-l",
        "--logs",
        dest="log_level",
        default="info",
        type=str,
        help="The base console logging level. Can be 'debug', 'info', 'warning' and 'error'. Defaults to 'info'.",
    )
    with timeit(lambda spanned: LOGGER.debug(f"Parsed commandline arguments in {1000*spanned:.4f} ms.")):
        options = parser.parse_args()
    return options.location, options.log_level


def _set_logger_level() -> None:
    """
    Simple function to update the logger console base level from commandline arguments.
    """
    global LOGGER
    log_level = _parse_args()[-1]
    LOGGER = logging_tools.get_logger(__name__, level_console=LEVELS_DICT[log_level])
    LOGGER.debug(f"Logger level set to {log_level}")


def _setup_output_directory(directory_name: str) -> pathlib:
    """
    Create an output directory with the provided name.

    Args:
        directory_name: A string with the name to give to the output directory.

    Returns:
        A `pathlib.Path` object of this directory.
    """
    directory = pathlib.Path(directory_name)
    if not directory.is_dir():
        LOGGER.debug(f"Creating output directory {directory.absolute()}")
        directory.mkdir()
    else:
        LOGGER.warning(f"Outputs directory {directory} already present. This may lead to unexpected behaviour.")
    return directory


# ==================================================================================================================== #


if __name__ == "__main__":
    crawl()
