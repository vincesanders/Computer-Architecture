import sys
'''
Bitwise operations
~ - bitwise NOT ex: ~x
& - bitwist AND ex: x & y
| - bitwise OR ex: x | y
~(&) - bitwise NAND (not AND): (AND inverted), when ONE is true or NONE is true ex: ~(x & y)
~(|) - bitwise NOR (not OR): (OR inverted), when neither are true ex: ~(x | y)
^ - bitwise XOR (exclusive OR): when only one is true ex: x ^ y

# Multi-bit numbers - Do operation bit by bit
    11101011    1 - true
&   10011101    1 - true
--------------------------
    10001001    1 - true AND true = true, so 1

    11011010
^   11100011
--------------
    00111001

# AND operations as a mask
    11010110
&   11110000 - ANDing a bitwith 1 will give you the bit's value, ANDing it with 0, will give you 0
--------------
    11010000

# shifting bitwise numbers - << and >>
     1111
<<1 11110 - fills in 0s for new bits

    1111
>>1  111 - removes last bit, other bits shift right.
'''

import sys

PRINT_NAME = 1
HALT = 2
SAVE_REGISTER = 3 # SAVE_REGISTER R1, 37   register[1] = 37
PRINT_REGISTER = 4
ADD = 5

memory = [0] * 256

register = [0] * 8 # 8 registers, like a variable

program = sys.argv[1]

with open(program) as f:
    address = 0
    for line in f:
        line = line.split("#")
        try:
            v = int(line[0])
        except ValueError:
            continue
        memory[address] = v
        address += 1


program_counter = 0
running = True

print(26 ^ 4)

while running:
    instruction_register = memory[program_counter]
    if instruction_register == PRINT_NAME:
        print('Vincent')
        program_counter += 1
    elif instruction_register == SAVE_REGISTER:
        register_number = memory[program_counter + 1]
        value = memory[program_counter + 2]
        register[register_number] = value
        program_counter += 3
    elif instruction_register == PRINT_REGISTER:
        register_index = memory[program_counter + 1]
        value = register[register_index]
        print(value)
        program_counter += 2
    elif instruction_register == ADD:
        register_index_one = memory[program_counter + 1]
        register_index_two = memory[program_counter + 2]
        value_one = register[register_index_one]
        value_two = register[register_index_two]
        register[register_index_one] = value_one + value_two
        program_counter += 3
    elif instruction_register == HALT:
        running = False
        program_counter += 1
    else:
        print(f'Unknown instruction {instruction_register} at address {program_counter}')
        sys.exit(1)