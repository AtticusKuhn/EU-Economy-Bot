from textblob import TextBlob
import nltk
import wikipedia
import re
from nltk.corpus import wordnet as wn
import random

nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')


def get_similar_words( word, page):
        synsets = wn.synsets(word, pos='n')# In the absence of a better method, take the first synset
        if len(synsets) == 0:# If there aren't any synsets, return an empty list
            return []
        else:
            synset = synsets[0]
        hypernym = synset.hypernyms()[0]# Get the hypernym for this synset (again, take the first)
        hyponyms = hypernym.hyponyms()        # Get some hyponyms from this hypernym
        similar_words = []        # Take the name of the first lemma for the first 8 hyponyms
        for hyponym in hyponyms:
            similar_word = hyponym.lemmas()[0].name().replace('_', ' ')
            if similar_word != word:
                similar_words.append(similar_word)
            if len(similar_words) == 8:
                break
        print("similar_words are,",similar_words)
        return similar_words
def evaluate_sentence(sentence,page):
    print("tags are",sentence.tags)
    if sentence.tags[0][1] == 'RB' or len(sentence) < 6:
        # This sentence starts with an adverb or is less than five words long
        # and probably won't be a good fit
        return None
    tag_map = {word.lower(): tag for word, tag in sentence.tags}
    replace_nouns = []
    for word, tag in sentence.tags:
        if tag == 'NN':# and word not in page.title:# For now, only blank out non-proper nouns that don't appear in the article title
            # Is it in a noun phrase? If so, blank out the last two words in that phrase
            
            for phrase in sentence.noun_phrases:
                if phrase[0] == '\'':
                    print("help me")
                    # If it starts with an apostrophe, ignore it
                    # (this is a weird error that should probably
                    # be handled elsewhere)
                    break

                if word in phrase:
                    # Blank out the last two words in this phrase
                    [replace_nouns.append(phrase_word) for phrase_word in phrase.split()[-2:]]
                    break

            # If we couldn't find the word in any phrases,
            # replace it on its own
            if len(replace_nouns) == 0:
                replace_nouns.append(word)
            break
            
    #if len(replace_nouns) == 0:
    #    # Return none if we found no words to replace
    #    return None

    trivia = {
        'title': page.title,
        'url': page.url,
        'answer': ' '.join(replace_nouns)
    }
    print("trivia is",trivia )

    if len(replace_nouns) == 1:
        # If we're only replacing one word, use WordNet to find similar words
        trivia['similar_words'] = get_similar_words(replace_nouns[0],page)
    else:
        # If we're replacing a phrase, don't bother - it's too unlikely to make sense
        trivia['similar_words'] = []

    # Blank out our replace words (only the first occurrence of the word in the sentence)
    replace_phrase = ' '.join(replace_nouns)
    blanks_phrase = ('__________ ' * len(replace_nouns)).strip()

    expression = re.compile(re.escape(replace_phrase), re.IGNORECASE)
    sentence = expression.sub(blanks_phrase, str(sentence), count=1)

    trivia['question'] = sentence
    return trivia

def subject_to_quiz(subject):
    title=subject
    page = wikipedia.page(title)
    blob = TextBlob(page.summary)
    #questions=[]
    sentence = random.choice(blob.sentences)
    #questions.append(evaluate_sentence(sentence, page))
    eval_res =evaluate_sentence(sentence, page)
    print(eval_res)
    return eval_res
