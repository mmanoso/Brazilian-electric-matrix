# Analisis of the Brazilian Electric Matrix

This Project take the data obtained in the official page of the Agência Nacional de Energia Elétrica (ANEEL) in the form of a list of electric generators and relevant information about each generator in a .CSV file. In a Jupyter Notebook, the data is analyzed and cleaned, and further stored in a .pkl format more suitable for being used in an application programed in Python using the library Streamlit among others.
Also, the analysis is performed with the Tableau and the Power BI programs, where the data is taken from the .CSV file, analyzed and transformed into a dynamic dashboard application like the Streamlit application.

## Jupyter Notebook analysis

Using the python programming and the jupyter notebook tools, the data is analyzed searching for null and duplicates values, analyzing the data types of each column, the unique values of interest of the different columns and quick graphs of the electric power vs different columns of interest, that will later be used in the Streamlit application.

## Streamlit application

An online application, that allows a final user to analyze the data with useful and dynamic graphics, to get insights related to the evolution of the electric matrix in Brazil, the actual state related to fuels type used, geographic distribution, total electric power installed, and the projects that are being constructed in July 2024 and the ones that are projected to be constructed in the future. This app allows the user to see the path taken by the Brazilian country related to its generation of electricity.

### This application can be found in the following GitHub link:

https://github.com/mmanoso/streamlit-app-brazil-electric-matrix

### The app is mounted in the Streamlit free cloud and can be used following this link:

https://mmanoso-app-brazil-electric-matrix.streamlit.app/

## Tableau analysis and application

In this project there is also a Tableau dashboard application like the Streamlit online app. Following the same principle but using another tool for visualization of the data.
The Tableau application consists of two dashboards to visualize the data. In the first page of the application, it can be visualized the geographic distribution of every electric generator in Brazil by its location points in the map, and a choropleth map to see the values of electric power installed by state. Also, the historical evolution of electric generation can be seen up to July 2024.
