# Classification : Email Filtering
##### --------------------------------------------------------------------------
#### Introduction -
Spam Classification is a document classification problem to classify the emails into whether they are spam or not.

#### Technique -
 We implemented Naive Bayes algorithm with MAP solutions.

 a) We created a bag of words from the training set of emails

 b) Calculated the MAP value for every word.
 MAP value =
 (frequency of the word in that class + m)/(total # of words in the class** + mV)

** duplicates are also counted

 Smoothening factor: m =1, V = total number of words in both classes

 c) Then we used the MAP value for prediction. We multiplied the MAP values of all the words in the document with the probability of the class i.e.
 (total emails in class spam or not spam)/(total number of emails in both classes)
 Prediction = max(Class spam, Class not spam)

 #### Code Description
 predict_with_map() : Prediction for test data using MAP solution value

 calc_map() : we create a dictionary of words in both classes as keys and values are MAP values for spam and not spam

 parse_file() : Parses over the train directory over all the files in both spam and not spam directories to create bag of words

 parse_directory() : Parse for spam and not spam training data

 #### Problem Faced -
 1) We had an error for UNICODE while reading certain files. We used encoding cp437 for it as it has all the coding characters.

 2)We first used html2text package which was not available on SICE server so we replaced it with a Regex for removing html tags from the document

 3)There were newline escape characters in the document which made words  look like "go\nto" which was in a wrong format to add to in bag of words. We removed it using Regex.

 4)As the decimal values were small (MAP values for words) the product was too small for the entire document making it -inf which could not give good predictions. We used log to solve this.

 #### Design Decision
 1)We rounded off the prediction value upto 8 decimal values.

 2)The product of MAP values were too small so instead we too log of the product making it sum of the log of MAP values for the words in the document.

 3)We used a smoothening factor on MaxL ratio to avoid '0' as prediction cannot be estimated as both classes will have prediction '0'

 4)List of words "Stop words" which are not relevant to email spam Ex.'the', 'to', 'Jan', 'Mon' were excluded from bag of words to lessen the running time. These words are in the text file "Irrelevant_words.txt"

 #### Observation:
 We checked our output for accuracy there are approximately 98 wrong prediction for the given data set of 2254 emails. Making the prediction approximately 94.24% accurate.
 The Running time for the algorithm is approx 30s for a training set of 10000 emails and test set of 2254 emails.

 #### References
[https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character](https://stackoverflow.com/questions/9233027/unicodedecodeerror-charmap-codec-cant-decode-byte-x-in-position-y-character)

[https://www.link-assistant.com/seo-stop-words.html](https://www.link-assistant.com/seo-stop-words.html)

#### Code Run :
```
/.spam.py
```
