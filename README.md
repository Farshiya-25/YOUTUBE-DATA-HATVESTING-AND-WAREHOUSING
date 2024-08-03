# Youtube data harvesting and warehousing using SQL and streamlit
**Introduction**

YouTube Data Harvesting and Warehousing is a project that aims to allow users to access and analyze data from multiple YouTube channels. The project utilizes SQL, MongoDB, and Streamlit to create a user-friendly application that allows users to retrieve, store, and query YouTube channel and video data.

**Project Overview**

The YouTube Data Harvesting and Warehousing project consists of the following components:

**Streamlit Application**: A user-friendly UI built using Streamlit library, allowing users to interact with the application and perform data retrieval and analysis tasks.

**YouTube API Integration**: Integration with the YouTube API to fetch channel and video data based on the provided channel ID.

**SQL Data Warehouse**: Migration of data to a SQL database, allowing for efficient querying and analysis using SQL queries.

**Data Analysis**: Presentation of retrieved data using Streamlit's data visualization features, enabling users to analyze the data.


**Technologies Used**:

The following technologies are used in this project:

**Python**: The programming language used for building the application and scripting tasks.
**Streamlit**: A Python library used for creating interactive web applications and data visualizations.
**YouTube API**: Google API is used to retrieve channel and video data from YouTube.
**SQL (MySQL)**: A relational database used as a data warehouse for storing migrated YouTube data.
**Pandas**: A data manipulation library used for data processing and analysis.


**Usage**:

Once the project is setup and running, users can access the Streamlit application through a web browser. The application will provide a user interface where users can perform the following actions:

-Enter a YouTube channel ID to retrieve data for that channel.
-Store the retrieved data in the MongoDB data lake.
-Collect and store data for multiple YouTube channels in the data lake.
-Select a channel and migrate its data from the data lake to the SQL data warehouse.
-Search and retrieve data from the SQL database using various search options.
-Perform data analysis using the provided features.

**Future Enhancements**:

Here are some potential future enhancements for the YouTube Data Harvesting and Warehousing project:

Authentication and User Management: Implement user authentication and management functionality to secure access to the application.
Scheduled Data Harvesting: Set up automated data harvesting for selected YouTube channels at regular intervals.
Advanced Search and Filtering: Enhance the search functionality to allow for more advanced search criteria and filtering options.
Additional Data Sources: Extend the project to support data retrieval from other social media platforms or streaming services.
Advanced-Data Analysis: Incorporate advanced analytics techniques and machine learning algorithms for deeper insights into YouTube data.
Export and Reporting: Add features to export data and generate reports in various formats for further analysis and sharing.

**Conclusion**:

The YouTube Data Harvesting and Warehousing project provides a powerful tool for retrieving, storing, and analyzing YouTube channel and video data. By leveraging SQL and Streamlit, users can easily access and manipulate YouTube data in a user-friendly interface. The project offers flexibility, scalability capabilities, empowering users to gain insights from the vast amount of YouTube data available.
