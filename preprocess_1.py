#need to install pyenchant first
from enchant.checker import SpellChecker
from nltk import pos_tag, pos_tag_sents ,word_tokenize, sent_tokenize
import re

def spellCheck(text):
	chkr = SpellChecker("en_US",text)
	for err in chkr:
		repls = chkr.suggest(err.word)
		if len(repls) > 0:
			repl = repls[0]
			err.replace(repl)
	return chkr.get_text()

def errCount(text):
	chkr = SpellChecker("en_US",text)
	count = 0
	for err in chkr:
		count += 1
	return count

stripTagSet = frozenset(['.','DT','FW', 'IN', 'LS', 'MD', 'NN','NNS','NNP','PDT','POS','PRP','RP','TO','UH','WDT'])
keepTagSet = frozenset(['JJ','JJR','JJS','RB','RBR','RBS','VB','VBD','VBG','VBN','VBP','VBZ'])
def toTaggedTokens(text):
	sent_tokens = [word_tokenize(t) for t in sent_tokenize(text)]
	return pos_tag_sents(sent_tokens)	

def stripTags(sentOfTokens,tags=stripTagSet):
    return [(tok,tag) for tok,tag in sentOfTokens if tag not in tags]

def keepTags(sentOfTokens,tags=keepTagSet):
	return [(tok,tag) for tok,tag in sentOfTokens if tag in tags]

def mergeNots(sentOfTokens):
	newSent = []
	isNot = False
	for toktag in sentOfTokens:
		tok, tag = toktag
		if tok == 'not':
			isNot = True
		else:
			if isNot:
				newSent.append(('not-' + tok,tag))
				isNot = False
			else:
				newSent.append(toktag)	
	return newSent

def tokenizeStripTags(text,tags=stripTagSet):
	ttokens = toTaggedTokens(text)
	return [item for sent in ttokens for item in stripTags(sent,tags)]


def tokenizeKeepTags(text,tags=keepTagSet):
	ttokens = toTaggedTokens(text)
	return [item for sent in ttokens for item in keepTags(sent,tags)]
	
def tokenizeMergeNotsAndReduce(text):
	ttokens = toTaggedTokens(text)
	stripped = [mergeNots(stripTags(sent)) for sent in ttokens]
	return [item for sent in stripped for item in keepTags(sent)]