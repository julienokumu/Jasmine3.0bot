import json
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
import random
import re

def clean_up_sentence(sentence):
    # Remove symbols
    sentence = re.sub(r"[\']|[\?]|[\.]|[\!]|[\,]", "", sentence)
    sentence = sentence.lower()  # Convert to lowercase
    sentence_words = nltk.word_tokenize(sentence)  # Use punkt tokenizer
    return sentence_words

def match_intent(sentence):
    with open('intents.json') as f:
        intents = json.load(f)

    sentence_words = clean_up_sentence(sentence)

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            pattern_words = clean_up_sentence(pattern)
            if all(word in sentence_words for word in pattern_words):
                return intent['tag']

    return 'unknown'

user_input = "Hi"
intent_tag = match_intent(user_input)
print(intent_tag)  # Output: greeting

def bag_of_words(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [1 if word in sentence_words else 0 for word in words]
    return bag

def predict_class(sentence):
    sentence_words = clean_up_sentence(sentence)
    scores = []
    for intent in intents['intents']:
        score = 0
        num_patterns = len(intent['patterns'])
        for pattern in intent['patterns']:
            words = nltk.word_tokenize(pattern)
            bag = bag_of_words(sentence, words)
            score += sum(bag)  # Calculate the sum of the bag of words
        score /= num_patterns  # Divide by the number of patterns
        scores.append(score)
    return scores

def get_response(sentence):
    intent_tag = match_intent(sentence)
    if intent_tag != 'unknown':
        for intent in intents['intents']:
            if intent['tag'] == intent_tag:
                responses = intent['responses']
                return random.choice(responses)
    else:
        return "I didn't understand that."
