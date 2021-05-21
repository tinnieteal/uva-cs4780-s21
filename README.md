# Mega - Matadata-based Search Engine (Information Retrieval Course Project)


## Introduction
💻 Mega is a matadata-based search engine that aims to provide different search options for users with different approaches. It includes three different ranking algorithms. Firstly, to serve the users who have clear ideas on what they need, i.e. searching about product name or brand names, we provide a search option, **Standard**, that solely matches product' titles and descriptions with users' query. Secondly, to serve the users who are not sure what products they want to buy, we provide an option, **With Comment**, that is based on not only products' titles and descriptions but also on other users' reviews. Lastly, we provide an option, **Mega**, that considers all three of the aforementioned aspects, but would additionally perform sentiment analysis on users' reviews --- the products with more positive reviews would be assigned with a higher weight on its reviews, and lower otherwise.The last option would fit the users who would thoroughly evaluate the reviews about a product in their decision-making. 


Additionally, Mega will display the products' titles, descriptions, and reviews with **highlights** on the terms that match the input queries in order to provide explainable recommendations. An ASIN number is also provided under each product's image for users to go directly to the product's page on Amazon. 

## Dataset
The UCSD Amazon Review Dataset under the category “All Beauty” is used Maga. After data cleaning and pre-processing, we are left with 4048 product items in the end. 

## Setup
`Clone` the current project from Github:

```
$ mkdir cs4780
$ git clone https://github.com/tinnieteal/uva-cs4780-s21.git
```
`Locate` the project file:
```
$ cd MAGA
```
`Run` Localhost:
```
$ python manage.py runserver
```
If you visit http://127.0.0.1:8000/, you should be able to see Maga ready to be tested!





