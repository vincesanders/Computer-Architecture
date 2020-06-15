/*
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
*/
const array = ['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']

const getIndex = length => length % 2 === 0 ? length / 2 : Math.ceil((length - 1) / 2)

array.sort((a, b) => a[getIndex(a.length)].localeCompare(b[getIndex(b.length)]));

for (s of array) {
    console.log(s)
}