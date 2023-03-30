# River Catchment

![Continuous Integration build in GitHub Actions](https://github.com/IRSD-Group1/rivercatchment/workflows/CI/badge.svg?branch=development)
![Issues Open](https://img.shields.io/github/issues/IRSD-Group1/rivercatchment)

## Introduction

This is a software project developed during the Earth Science focused [Intermediate Research Software Development Skills In Python](https://github.com/UoMResearchIT/python-intermediate-development-nerc) course 2023.

----------
## Purpose

The project involve the analysis of environmental measurement data to improve our understanding of the hydrological, hydrogeological, geomorphological and ecological interactions within permeable catchment systems. The projects uses baseline datasets from the Lowland Catchment Research (LOCAR) Programme.

---------------
## Architecture

### **Model-View-Controller (MVC) Architecture**

> MVC architecture divides the related program logic into three interconnected modules:

Model (data), View (client interface), and
Controller (processes that handle input/output and manipulate the data).

- **Model** represents the data used by a program and also contains operations/rules for manipulating and changing the data in the model. This may be a database, a file, a single data object or a series of objects - for example a table representing patients’ data.

- **View** is the means of displaying data to users/clients within an application (i.e. provides visualisation of the state of the model). For example, displaying a window with input fields and buttons (Graphical User Interface, GUI) or textual options within a command line (Command Line Interface, CLI) are examples of Views. They include anything that the user can see from the application. While building GUIs is not the topic of this course, we will cover building CLIs in Python in later episodes.

- **Controller** manipulates both the Model and the View. It accepts input from the View and performs the corresponding action on the Model (changing the state of the model) and then updates the View accordingly. For example, on user request, Controller updates a picture on a user’s GitHub profile and then modifies the View by displaying the updated profile back to the user.

--------
## Tests

Several tests have been implemented already, some of which are currently failing.
These failing tests set out the requirements for the additional code to be implemented during the workshop.

The tests should be run using `pytest`, which will be introduced during the workshop.

--------
## Prerequisites
- [Numpy](https://numpy.org)
- [Pandas](https://pandas.pydata.org)
- [Geopandas](https://geopandas.org/en/stable/)