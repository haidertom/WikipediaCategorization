import languageProcess as lp

path = '../DataSnippets/Baseline/Space/wiki/AA/wiki_00'
lang = lp.languageProcess(path)
test = lang.getHighFreqWords()
print(len(test))