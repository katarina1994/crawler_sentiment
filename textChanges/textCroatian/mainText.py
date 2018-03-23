
'''
Created on 23. ozu 2018.

@author: Katarina123
'''

import codecs
from text_hr import utils

fStopWords = codecs.open("stopWords.txt", 'w', encoding='Windows-1250')

for word_base, l_key, cnt, _suff_id, wform_key, wform in utils.get_all_std_words():
    print word_base, l_key, cnt, _suff_id, wform_key, wform
    if(wform):
        #wform = unicode(wform, "utf-8")
        fStopWords.write(wform.encode('Windows-1250', 'replace').decode('Windows-1250', 'replace') + "\n")
    else:
        #word_base = unicode(word_base, "utf-8")
        fStopWords.write(word_base.encode('Windows-1250', 'replace').decode('Windows-1250', 'replace') + "\n")
        
fStopWords.close()
