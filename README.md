# Disaster Response Pipelines
This project was made in an effort to classify messages sent during disasters in order to direct those messages to the appropriate response agencies.

This project consists of 2 pipelines and a web app. The first pipeline processes data from Figure Eight containing messages and associated categories, and saves that data to an SQL database. The second pipeline builds a model which assigns any combination of 36 categories to a given message. The web app allows you to interface with the model, giving you the ability to input a message which the model will then categorize. The web app also features some information about the data set which should help you to write your messages.

### File Structure
```
.
├── app
│   ├── static
│   │   ├── stylesheet.css
│   ├── templates
│   │   ├── master.html
│   └── run.py
├── data
│   ├── DisasterResponse.db
│   ├── disaster_categories.csv
│   ├── disaster_messages.csv
│   └── process_data.py
├── models
│   ├── classifier.pkl
│   └── train_classifier.py
├── models
│   └── universal_functions.py
└── README.md
```

### Usage
The general order of operations for using this project should be the first: process the data, second: train the classifier and third: run the web app. However you can also run the web app without going through the first or the first 2 steps, as I have included a premade database in the data folder and a pretrained classifier in the models folder. The default commands to run these scripts are below, though do note that the script runs relative to your terminal's current working directory.

```
python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db # Process the data.
python train_classifier.py ../data/DisasterResponse.db classifier.pkl                    # Train the classifier.
python run.py classifier.pkl ../data/DisasterResponse.db ../models/classifier.pkl        # Run the web app.
```

You can then connect to the web app through the port 3001. Once in the web app you will be met by a grid containing the names of each of the 36 categories. On the left there will be a text box in which you can enter a message you would like to classify. Once classified any category into which the message fits will be highlighted in green. Lastly you'll see two visualisations below the main interface which, if I've done my job right, should be self explanatory.

### How it works
Now that we have a brief overview of the pipeline, let's look at each step in detail. First we'll discuss the data processing step.

The first action taken in the data processing step is to load the data. The data is split into 2 tables: messages and categories. These tables are joined as soon as they're loaded. Some simple text processing is used to convert the categories-which are encoded as single strings-into features. Any duplicate messages are then removed; with the duplicate that has the most categories being preserved. Additionally a separate table is generated containing the 20 most common words across all of the messages. Of note is that the text processing method used means that if a category is never applied to a message, that category does not become a feature in the final table. To compensate for this, a blank message that is classified as every category is added and subsequently removed from the dataframe in order to "initialize" each feature.

Once the data is processed it can then be used to train the classifier. The data is first split 80/20 into train and test sets respectively. The type of classifier used, as well as some hyperparameters of each classifier, are selected by simply testing each posible combination. Using cross validation, the best combination of hyperparameters for the best classifier is selected and that model is then exported into a pickle file. Note here that the range of useable classifiers was significantly reduced by the inclusion of features with only one value, specifically the "child_alone" column.

Now that the classifier is trained, the backend of the web app is complete, and the web app can be run. The main feature of the web app (the ability to classify messages), uses the pickled classifier to predict the categorization of the provided messages. As for the visualizations, the first (representing the amount of messages that had 0, 1, 2... etc. categories attributed to them) was made by simply summing the features for each row. The second visualization uses the most common words table that was made in the data processing step.

### Sources
[Appen](https://appen.com/): I got this data from Figure Eight through Udacity. Figure Eight has since been aquired by Appen and their URL now redirects to Appen so that is probably where they'd like me to send you now.

### Dependencies
- [NumPy](https://pypi.org/project/numpy/): Package for array computing with Python.
- [Pandas](https://pypi.org/project/pandas/): Python package that provides fast, flexible, and expressive data structures.
- [Plotly](https://pypi.org/project/plotly/): An open-source, interactive data visualization library for Python.
- [Natural Language Toolkit](https://pypi.org/project/nltk/): Python package for natural language processing.
- [scikit-learn](https://pypi.org/project/scikit-learn/): A set of python modules for machine learning and data mining.
- [Flask](https://pypi.org/project/Flask/): A simple framework for building complex web applications.
- [Bootstrap](https://getbootstrap.com/): The most popular framework for building responsive, mobile-first sites.
