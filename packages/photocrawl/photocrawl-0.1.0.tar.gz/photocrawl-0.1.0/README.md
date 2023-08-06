# PhotoCrawl: A Photography Analyzer

A simple script to run analysis and get insight on my use of equipment and settings in my practice of photography.

## Install

### Prerequisites

This script runs on Python3.6+, and requires the following libraries: [`PyExifInfo`][pyexifinfo], `matplotlib`, `seaborn`,  and `pandas`.
It also requires that you have the amazing [ExifTool][exiftool] package by Phil Harvey.

### Install

This code is compatible with `Python 3.6+`.
If for some reason you have a need for it, you can simply install it in your virtual enrivonment with:
```bash
pip install photocrawl
```

You can also clone this repository through VCS, and install it into a virtual environment.
With `git`, this would be:
```bash
git clone https://github.com/fsoubelet/PyhDToolkit.git
cd PhotoCrawl
make
```

## Usage

With this package is installed in the activated enrivonment, usage is:
````bash
python -m photocrawl -i files_location
````

The script will crawl files, extract exif and output visualizations named `insight_1.jpg` and `insight_2.jpg` in a newly created `outputs` folder.

## Output example

Here is an example of what the script outputs:

<p align="center">
  <img src="https://github.com/fsoubelet/PhotoCrawl/blob/master/example_outputs/insight_1.jpg"/>
</p>

<p align="center">
  <img src="https://github.com/fsoubelet/PhotoCrawl/blob/master/example_outputs/insight_2.jpg"/>
</p>

## TODO

- [x] Handling raw files.
- [x] Handling subfolders when looking for files.
- [x] Output all insight in a single/two plot.
- [x] Make into a package

## License

Copyright &copy; 2019-2020 Felix Soubelet. [MIT License][license]

[exiftool]: https://www.sno.phy.queensu.ca/~phil/exiftool/
[license]: https://github.com/fsoubelet/PhotoCrawl/blob/master/LICENSE 
[pyexifinfo]: https://github.com/guinslym/pyexifinfo