# Furniture Store
## Database and dummy data generator

This project was first created for a Database And Knowledge Base course assignment; for this release on Github I decided to maintain its original design, only correcting minor mistakes to try and improve its overall performances.

The idea was to develop a solution to help the management of a chain of furniture stores distributed over the Italian territory. I wanted to keep track of various data, from the inventory and personnel of each store to statistics concerning the shopping habits of the clients.

The project wants to provide a general framework and management of the following aspects:
- Management of individual stores and their employees
- Management of furniture, prices, and production status
- Customer information
- Sales history

After analyzing the requirements, and a couple of iteration on the design later, this is the physical data model that represents the current database:

![physical data model](/docs/schema.png)

## API Implementation
After I completed the design of the database and filled it with random generated data, I thought it would be nice to easily access the information from an online Admin dashboard, to manage furniture inventory and sales data. Before starting to develop the frontend, we need some APIs that can connect to the database and retrieve the relevant data to then dynamically generate some graphs.

I decided to use C# and ASP.NET to develop a couple of simple APIs that could be used to generate useful graphs (for example, one returns the total amount of money spent by loyalty card owners, both by region and by province of residence).

## Technologies

- [MySQL] - One of the requirements in the original course assignment was to create the Database in MySql; in the database folder, the two .sql files create the Database and all its tables, and add a couple of useful triggers to help maintain its consistency
- [Python] - The Python code is used to generate random, but plausible, dummy data that can be used to test the database.
- [C# ASP.NET] - Used to design and develop the backend APIs.

## Installation

You can execute the SQL code contained in the .sql files to create your database. It's default name will be baldonifurniturestore.
The fillDatabase.py file can be edited to your needs:
```
db = mysql.connector.connect(
    host="localhost",
    database = "baldonifurniturestore",
    user="root",
    passwd="root"               
)
```
You can change the values to fit your needs, and the program will automatically fill the database with dummy data. Note that some computers may take a long time to execute all the queries, since the code is written to create a fair amount of rows for each table (see notes for more details).

## Notes 
#### Randomness
When filling some tables, random is added on purpose to try and simulate different scenarios and to test the capabilities of the database (for example, the code will always create 1000 different furniture items, but it will create a random number of card holders for each region, with a total number of rows somewhere in the 4,000-30,000 range). Numbers can be further tweaked to see how the database performs complex queries on a bigger dataset.

#### Weighted probabilities in randomness
The program is not written to produce semi-realistic scenarios; for example, I could have loaded into the municipalities data the population of each municipality, and use it to assign to more populated cities a higher probability to be chosen as the location of a store. In the end I decided against adding such features, being out of the scope of this particular project.

## Credits
The data that fills the Regions, Provinces and Municipalities tables are extracted from .json files from the repository [Italia](https://github.com/napolux/italia) created by user [Napolux](https://github.com/napolux)
