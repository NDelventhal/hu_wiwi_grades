

<!-- TOC -->
## Table of Content
- [hu_wiwi_grades](#hu_wiwi_grades) 
- [Background](#background)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [License](#license)
<!-- /TOC -->

## hu_wiwi_grades
**hu_wiwi_grades** is a Python library for searching, viewing and scraping published students' grading of the Faculty of Economics and Business Administration of the Humboldt University of Berlin.

Please note: The functionality maybe interrupted in case any changes in the publication occur or in case the website is not available.  

## Background

This library was primarily created for testing/training purposes, such as extracting information from PDF files, writing and publishing of code. It nevertheless aims to offer a use-case. Current and historical grading information may be of interest for (prospective) students, examiners or potentially even employers.   

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install hu_wiwi_grades

```python
pip install hu_wiwi_grades
```
Or install it through the author's Github repository 

```python
pip install git+https://github.com/NDelventhal/hu_wiwi_grades
```

## Requirements 

The following libraries are required: 
- tabula
- pandas
- numpy
- requests 
- beautifulsoup4

These libraries can be installed via the package manager [pip](https://pip.pypa.io/en/stable/).

```python
pip install tabula numpy pandas requests beautifulsoup4
```

## Usage

```python

import hu_wiwi_grades as hu

hu.list_sources() 
# scrapes URL sources that list grading overviews and returns a dictionary containing the semesters as keys and the URLs as values. 

df = hu.scrape_overview(exam = "Economics") 
# Scrapes the latest grading overview and returns the overview or a subset based on the entered exam specification.
# In this example solely Economics exams are returned. The exam arguments defaults to "" (no filtering).  

df = hu.scrape_all_overviews(exam = "Valuation") 
# Same as above, but instead of solely the latest overview all historical overviews are pulled. Typically, a few semesters are available.

df = hu.get_grading(exam="", only_current_semester = True) 
# Scrapes the grades from the URLs listed in the overview pages of either only the latest semester (only_current_semester = True) or all (only_current_semester = False). 
# An exam filter may be specified as in the examples above or not.
# Returns a dataframe listing the number of participants, the examiner and all grades as variables. 

df2 = hu.prepare_for_analysis(df) 
# Prepares the dataframe output of get_grading() for further analysis, such as visualisations, descriptive statistics or regression analysis.

```

Further usuage examples are listed [here](https://github.com/NDelventhal/hu_wiwi_grades/blob/main/documentation/usage_examples.ipynb)

## License

This project is licensed under the [MIT License](https://github.com/NDelventhal/hu_wiwi_grades/blob/main/LICENSE).

## Contact

- The author: Niall Delventhal - ni.delventhal@gmail.com

