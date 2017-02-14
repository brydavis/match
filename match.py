
import re
from itertools import groupby
from __future__ import division


# http://www.mibgroup.com/pdf/settlement_search_info.pdf
# http://www.oracle.com/webfolder/technetwork/data-quality/edqhelp/Content/processor_library/matching/comparisons/date_transposition_match.htm





# https://rosettacode.org/wiki/Jaro_distance#Python
def jaro(s, t):
    s_len = len(s)
    t_len = len(t)
 
    if s_len == 0 and t_len == 0:
        return 1
 
    match_distance = (max(s_len, t_len) // 2) - 1
 
    s_matches = [False] * s_len
    t_matches = [False] * t_len
 
    matches = 0
    transpositions = 0
 
    for i in range(s_len):
        start = max(0, i-match_distance)
        end = min(i+match_distance+1, t_len)
 
        for j in range(start, end):
            if t_matches[j]:
                continue
            if s[i] != t[j]:
                continue
            s_matches[i] = True
            t_matches[j] = True
            matches += 1
            break
 
    if matches == 0:
        return 0
 
    k = 0
    for i in range(s_len):
        if not s_matches[i]:
            continue
        while not t_matches[k]:
            k += 1
        if s[i] != t[k]:
            transpositions += 1
        k += 1
 
    return ((matches / s_len) +
            (matches / t_len) +
            ((matches - transpositions/2) / matches)) / 3
 
for s,t in [(   'MARTHA',      'MARHTA'),
            (    'DIXON',    'DICKSONX'),
            ('JELLYFISH',  'SMELLYFISH')]:
    print("jaro(%r, %r) = %.10f" % (s, t, jaro(s, t)))




# https://rosettacode.org/wiki/NYSIIS#Python
_vowels = 'AEIOU'

def replace_at(text, position, fromlist, tolist):
    for f, t in zip(fromlist, tolist):
        if text[position:].startswith(f):
            return ''.join(
            	[text[:position],
				t,
				text[position+len(f):]],
			)
    return text
 
def replace_end(text, fromlist, tolist):
    for f, t in zip(fromlist, tolist):
        if text.endswith(f):
            return text[:-len(f)] + t
    return text
 
def nysiis(name):
    name = re.sub(r'\W', '', name).upper()
    name = replace_at(name, 0, ['MAC', 'KN', 'K', 'PH', 'PF', 'SCH'],
                               ['MCC', 'N',  'C', 'FF', 'FF', 'SSS'])
    name = replace_end(name, ['EE', 'IE', 'DT', 'RT', 'RD', 'NT', 'ND'],
                             ['Y',  'Y',  'D',  'D',  'D',  'D',  'D'])
    key, key1 = name[0], ''
    i = 1
    while i < len(name):
        #print(i, name, key1, key)
        n_1, n = name[i-1], name[i]
        n1_ = name[i+1] if i+1 < len(name) else ''
        name = replace_at(name, i, ['EV'] + list(_vowels), ['AF'] + ['A']*5)
        name = replace_at(name, i, 'QZM', 'GSN')
        name = replace_at(name, i, ['KN', 'K'], ['N', 'C'])
        name = replace_at(name, i, ['SCH', 'PH'], ['SSS', 'FF'])
        if n == 'H' and (n_1 not in _vowels or n1_ not in _vowels):
            name = ''.join([name[:i], n_1, name[i+1:]])
        if n == 'W' and n_1 in _vowels:
            name = ''.join([name[:i], 'A', name[i+1:]])
        if key and key[-1] != name[i]:
            key += name[i]
        i += 1
    key = replace_end(key, ['S', 'AY', 'A'], ['', 'Y', ''])
    return key1 + key
 




# https://www.rosettacode.org/wiki/Soundex#Python
def soundex(word):
   codes = ("bfpv","cgjkqsxz", "dt", "l", "mn", "r")
   soundDict = dict((ch, str(ix+1)) for ix,cod in enumerate(codes) for ch in cod)
   cmap2 = lambda kar: soundDict.get(kar, '9')
   sdx =  ''.join(cmap2(kar) for kar in word.lower())
   sdx2 = word[0].upper() + ''.join(k for k,g in list(groupby(sdx))[1:] if k!='9')
   sdx3 = sdx2[0:4].ljust(4,'0')
   return sdx3
 



 if __name__ == '__main__':
    names = ['Bishop', 'Carlson', 'Carr', 'Chapman', 'Franklin',
             'Greene', 'Harper', 'Jacobs', 'Larson', 'Lawrence',
             'Lawson', 'Louis, XVI', 'Lynch', 'Mackenzie', 'Matthews',
             'McCormack', 'McDaniel', 'McDonald', 'Mclaughlin', 'Morrison',
             "O'Banion", "O'Brien", 'Richards', 'Silva', 'Watkins',
             'Wheeler', 'Willis', 'brown, sr', 'browne, III', 'browne, IV',
             'knight', 'mitchell', "o'daniel"]
    for name in names:
        print('%15s: %s' % (name, nysiis(name)))
