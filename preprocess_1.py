#need to install pyenchant first
from enchant.checker import SpellChecker
from nltk import pos_tag, word_tokenize
import re

def spellCheck(text):
	chkr = SpellChecker("en_US",text)
	for err in chkr:
		repl = chkr.suggest(err.word)[0]
		err.replace(repl)
	return chkr.get_text()

def errCount(text):
	chkr = SpellChecker("en_US",text)
	count = 0
	for err in chkr:
		count += 1
	return count

stripTags = frozenset(['FW', 'IN', 'LS', 'MD', 'NN','NNS','NNP','PDT','POS','PRP','RP','TO','UH','WDT'])

def tokenizeStripTags(text,stripTags=stripTags):
    # remove non letters
    text = re.sub("[^a-zA-Z\s]", "", text)
    # tokenize
    tagged_tokens = pos_tag(word_tokenize(text))
    tokens = [tok for tok,tag in tagged_tokens if tag not in stripTags]
    return tokens