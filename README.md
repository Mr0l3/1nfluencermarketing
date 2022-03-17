# Theoretical Test
### 1. Differentiate Machine Learning, artificial intelligence, and data science.
Data Science is a field that is aimed in using data to bring crucial insights. Inside the huge amount of techniques used in Data Science, we can find Machine Learning, a subsection of Artificial Intelligence.

Artificial Intelligence is the field of study focused in replicating human intelligence in the machines.

Machine Learning is a subsection of Arficial Intelligence. It focuses in using learning techniques, so that the machine can learn by itself based on the data given.


### 2. What is the difference between linear regression and logistic regression?
Linear regression is used mainly, in regression problems, that is, we wat to predict a value based in a given input e.g. the price of a car based on the HP.

Logistic regression is used mainly, in binary classification problems e.g. determine whether the stock price is going to go up or down.


### 3. Explain the curse of dimensionality?
States that the amount of samples needed grows exponentially with dataset dimensionality. In another words, the error and the training time for a ML algorithm tends to increase with the number of features e.g. name, hair color, age; in the dataset. The algorithms are harder to design and harder to train.

### 4. What are precision, recall, f-measure, and roc? Explain what they are and when they are used
Precision is the correct guesses percentage of a guess set e.g. the algorithm found 10 cats, but only 8 were actually cats, so the precision is 8/10 = 0.8. We use Precision to measure false positives level.

Recall is the correct guesses percentage of a set e.g. from a set of 10 cats, the algorithm correctly found 4 cats, so the recall is 4/10 = 0.4. We use Recall to measure the detection level.

f-measure is the harmonic mean of precision and recall. It's used to measure the performance of a binary classifier.

ROC is graph that relates the true positives rate with the false negatives rate, along with the treshold variation. ROC allow us to find the optimal treshold that fit ours need.

### 5. What is the difference between train set, test set, and validation set?
Train set is the set used to train the model. Test set is the set used to evaluate the final model. The validation test is used to evaluate the model during training fase, this way, we're able to detect if the model has stopped learning and so on.

### 6. What is the p-value? It's a reliable measurement? How can we be sure?
p-value measures the probability of having random data and not data affected by something. It's a value used to determine if the data is affected by something or if the data is just random.

### 7. What is PCA?
Is a method used to reduce dimensionality. The idea is to reduce the variables amount while keeping as much information as possible.

# Practical test

### Explain what metrics are more representative (would better represent the user profile) and why.

- Followers: they represent the profile's reach
- Median of tweets for each time period: medians are strong to outliers, so outliers don't affected medians too much. Tweets represent the profile activity level in Tweeter.
- Plots: they are the main information source, mainly in more recent dates. With plots we can detect the profile's activity in the last days, weeks or months.

## Installation and usage
*Disclaimer: the pages may take a while to load since the application doesn't use concurrency and pararelism*
### venv setup
```python -m venv env```

### venv activation
```source env/bin/activate```

### Install dependencies:

```pip3 install -r requirements.txt```


### To run (with venv activated):
Change to flask directory

```cd flaskr```

Give execution permition to start script

```chmod +x startapp.sh```

Run the app

```./startapp.sh```
