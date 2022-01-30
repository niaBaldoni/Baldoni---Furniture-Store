CREATE DATABASE BaldoniFurnitureStore;

USE BaldoniFurnitureStore;

CREATE TABLE Regions (
	Region_Id 	INTEGER 	    NOT NULL,
    Region_Name VARCHAR(100)    NOT NULL,
    PRIMARY KEY (Region_Id)
    );
    
CREATE TABLE Provinces (
	Province_Id 	INTEGER 	    NOT NULL,
    Province_Name 	VARCHAR(100)    NOT NULL,
    Region_Id 		INTEGER 	    NOT NULL,
    PRIMARY KEY (Province_Id),
    FOREIGN KEY (Region_Id) 	REFERENCES Regions (Region_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );
    
CREATE TABLE Municipalities (
	Municipality_Id 	INTEGER 	    NOT NULL,
	Municipality_Name   VARCHAR(100)    NOT NULL,
	Province_Id         INTEGER 	    NOT NULL,
	PRIMARY KEY (Municipality_Id),
	FOREIGN KEY (Province_Id) 	REFERENCES Provinces (Province_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );

CREATE TABLE Stores (
	Store_Id 	    INTEGER 		NOT NULL,
	Store_Name      VARCHAR (150) 	NOT NULL,
	Municipality_Id INTEGER 		NOT NULL,
	PRIMARY KEY (Store_Id), 
	FOREIGN KEY (Municipality_Id) 	REFERENCES Municipalities (Municipality_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );

CREATE TABLE Departments (
	Department_Id 	INTEGER 	    NOT NULL,
    Deparment_Name 	VARCHAR(100) 	NOT NULL,
    PRIMARY KEY (Department_Id)
    );
    
CREATE TABLE Employees (
	Employee_Id 		INTEGER 	NOT NULL,
    Employee_Name 		VARCHAR(100) NOT NULL,
    Employee_Surname 	VARCHAR(100) NOT NULL,
    Hire_Date 			DATE 		NOT NULL,
    Store_Id 			INTEGER 	NOT NULL,
    Department_Id 		INTEGER 	NOT NULL,
    Manager 			BOOLEAN 	NOT NULL 	DEFAULT (0),
    PRIMARY KEY (Employee_Id),
    FOREIGN KEY (Store_Id) 		REFERENCES Stores (Store_Id) ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (Department_Id) REFERENCES Departments (Department_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );
    
CREATE TABLE Cards (
	Card_Id 		INTEGER		 NOT NULL,
    Card_Name 	    VARCHAR(100) NOT NULL,
    Card_Surname 	VARCHAR(100) NOT NULL,
    Birthday 		DATE 		 NOT NULL,
    Municipality_Id INTEGER 	NOT NULL,
    Points 			INTEGER 	NOT NULL 	DEFAULT (0),
    PRIMARY KEY (Card_Id),
    FOREIGN KEY (Municipality_Id) 	REFERENCES Municipalities (Municipality_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );
    
CREATE TABLE Transactions (
	Transaction_Id   INTEGER    NOT NULL,
    Transaction_Date DATETIME   NOT NULL,
    Total            DOUBLE     NOT NULL DEFAULT (0),
    Store_Id         INTEGER    NOT NULL,
    Card_Id          INTEGER,
    PRIMARY KEY (Transaction_Id),
    FOREIGN KEY (Store_Id) REFERENCES Stores (Store_Id) ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (Card_Id) REFERENCES Cards (Card_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );
    
CREATE TABLE Categories (
	Category_Id     INTEGER     NOT NULL,
    Category_Name   VARCHAR(100) NOT NULL,
    PRIMARY KEY (Category_Id)
    );
    
CREATE TABLE Furniture (
	Furniture_Id    INTEGER         NOT NULL,
    Furniture_Name  VARCHAR(100)    NOT NULL,
    Category_Id     INTEGER         NOT NULL,
    Discontinued    BOOLEAN         NOT NULL DEFAULT (0),
    Furniture_Height INTEGER        NOT NULL,
    Furniture_Width INTEGER         NOT NULL,
    Furniture_Depth INTEGER         NOT NULL,
    PRIMARY KEY (Furniture_Id),
    FOREIGN KEY (Category_Id) REFERENCES Categories (Category_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );
    
CREATE TABLE Fur_Sto (
	Furniture_Id    INTEGER,
    Store_Id        INTEGER,
    Quantity        INTEGER     NOT NULL DEFAULT (0),
    PRIMARY KEY (Furniture_Id, Store_Id),
    FOREIGN KEY (Furniture_Id) REFERENCES Furniture (Furniture_Id) ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (Store_Id) REFERENCES Stores (Store_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );
    
CREATE TABLE Prices (
	Furniture_Id    INTEGER     NOT NULL,
    Start_Date      DATETIME    NOT NULL DEFAULT '1970-01-01 00:00:01',
    End_Date        DATETIME    NOT NULL DEFAULT '2038-01-19 03:14:07',
    Price           DOUBLE      NOT NULL,
    Discount        INTEGER     NOT NULL DEFAULT (100),
    PRIMARY KEY (Furniture_Id, Start_Date),
    FOREIGN KEY (Furniture_Id) REFERENCES Furniture (Furniture_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );
    
CREATE TABLE Fur_Tra (
	Furniture_Id    INTEGER     NOT NULL,
    Transaction_Id  INTEGER     NOT NULL,
    Quantity        INTEGER     NOT NULL DEFAULT (0),
    PRIMARY KEY (Furniture_Id, Transaction_Id),
    FOREIGN KEY (Furniture_Id) REFERENCES Furniture (Furniture_Id) ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (Transaction_Id) REFERENCES Transactions (Transaction_Id) ON DELETE NO ACTION ON UPDATE CASCADE
    );