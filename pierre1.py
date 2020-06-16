import math
'''
Print out all of the strings in the following array in alphabetical order, each on a separate line.
['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']
The expected output is:
'Cha Cha'
'Foxtrot'
'Jive'
'Paso Doble'
'Rumba'
'Samba'
'Tango'
'Viennese Waltz'
'Waltz'
You may use whatever programming language you’d like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process
'''
# array = ['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']

# array.sort()

# for s in array:
#     print(s)

'''
Print out all of the strings in the following array in alphabetical order sorted by the middle letter of each string, each on a separate line. If the word has an even number of letters, choose the later letter, i.e. the one closer to the end of the string.
['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']
The expected output is:
'Cha Cha'
'Paso Doble'
'Viennese Waltz'
'Waltz'
'Samba'
'Rumba'
'Tango'
'Foxtrot'
'Jive'
You may use whatever programming language you’d like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.
'''

# iter through arr get middle letter, create dict
# sort keys in dict
# iter through sorted keys

array = ['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']

array_dict = {}

middle_chars = []

for s in array: # O(n)
    char_index = len(s) // 2
    char = s[char_index]
    if char in array_dict:
        array_dict[char].append(s)
    else:
        middle_chars.append(char)
        array_dict[char] = [s]

middle_chars.sort() # O(nlogn) < - time complexity

for char in middle_chars: # O(n)
    if len(array_dict[char]) > 1:
        for char in array_dict[char]:
            print(char)
    else:
        print(array_dict[char][0])