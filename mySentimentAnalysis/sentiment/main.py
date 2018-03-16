import nltk
nltk.download()
from nltk.classify import NaiveBayesClassifier

 
def word_feats(word):
    return dict([(word, True)])
 
positive_vocab = [ 'awesome', 'outstanding', 'fantastic', 'good', 'nice', 'great', 'perfect', 'love']
negative_vocab = [ 'bad', 'terrible','useless', 'hate', 'awfull']
neutral_vocab = [ 'movie','the','sound','was','is','actors','did','know','words','not', 'cloud']
 
positive_features = [(word_feats(pos), 'pos') for pos in positive_vocab]
negative_features = [(word_feats(neg), 'neg') for neg in negative_vocab]
neutral_features = [(word_feats(neu), 'neu') for neu in neutral_vocab]
 
train_set = negative_features + positive_features + neutral_features
#print (train_set)
classifier = NaiveBayesClassifier.train(train_set) 
 

neg = 0
pos = 0
sentence = "Terrible movie, but I love the music. Actors are useless and bad,but songs are nice."
sentence = sentence.lower()
words = sentence.split(' ')
for word in words:
    classResult = classifier.classify( word_feats(word))
    if classResult == 'neg':
        neg = neg + 1
    if classResult == 'pos':
        pos = pos + 1

print('Positive: ' + str(float(pos)/(pos+neg)))
print('Negative: ' + str(float(neg)/(pos+neg)))