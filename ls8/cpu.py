"""CPU functionality."""

import sys
from os import path

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.RAM = [0] * 256
        self.REG = [0] * 8
        self.PC = 0 # Program Counter
        self.IR = 0 # Instruction Register
        self.MAR = 0 # Memory Address Register
        self.MDR = 0 # Memory Data Register
        self.FL = 0
        self.IM = 0
        self.IS = 0
        self.SP = 0xF4  # 244
        self.running = False
        self.instructions = {
            0b10000010: self.handle_LDI,
            0b10000011: self.handle_LD,
            0b01000111: self.handle_PRN,
            0b10100010: self.handle_MUL,
            0b10100000: self.handle_ADD,
            0b10101110: self.handle_ADDI,
            0b10101000: self.handle_AND,
            0b01010000: self.handle_CALL,            
            0b10100111: self.handle_CMP,
            0b01100110: self.handle_DEC,
            0b10100011: self.handle_DIV,
            0b00000001: self.handle_HLT,
            0b01100101: self.handle_INC,
            0b01010010: self.handle_INT,
            0b01010101: self.handle_JEQ,
            0b01011010: self.handle_JGE,
            0b01010111: self.handle_JGT,
            0b01011001: self.handle_JLE,
            0b01011000: self.handle_JLT,
            0b01010100: self.handle_JMP,
            0b01010110: self.handle_JNE,
            0b10100100: self.handle_MOD,
            0b01101001: self.handle_NOT,
            0b00000000: self.handle_NOP,
            0b10101010: self.handle_OR,
            0b01000110: self.handle_POP,
            0b01001000: self.handle_PRA,
            0b01000101: self.handle_PUSH,
            0b00010001: self.handle_RET,
            0b10101100: self.handle_SHL,
            0b10101101: self.handle_SHR,
            0b10000100: self.handle_ST,
            0b10100001: self.handle_SUB,
            0b10101011: self.handle_XOR,
        }
        self.alu_operations = {
            'MUL': self.ALU_MUL,
            'ADD': self.ALU_ADD,
            'AND': self.ALU_AND,
            'CMP': self.ALU_CMP,
            'DEC': self.ALU_DEC,
            'DIV': self.ALU_DIV,
            'INC': self.ALU_INC,
            'MOD': self.ALU_MOD,
            'NOT': self.ALU_NOT,
            'OR': self.ALU_OR,
            'SHL': self.ALU_SHL,
            'SHR': self.ALU_SHR,
            'SUB': self.ALU_SUB,
            'XOR': self.ALU_XOR,
        }

    def load(self):
        """Load a program into memory."""

        self.MAR = 0

        program = sys.argv[1]

        with open(program) as file:
            for line in file:
                line = line.split("#")
                try:
                    self.MDR = int(line[0], 2)
                except ValueError:
                    continue
                self.ram_write(self.MDR, self.MAR)
                self.MAR += 1
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # while self.MAR < len(program):
        #     self.MDR = program[self.MAR]
        #     self.ram_write(self.MDR, self.MAR)
        #     self.MAR += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op in self.alu_operations:
            self.alu_operations[op](reg_a, reg_b)
        else:
            raise Exception("Unsupported ALU operation")

    def bitwise_addition(self, num1, num2): # recursive
        if num2 <= 0:
            return num1
        else: #                          sum of bits   common bits and shift
            return self.bitwise_addition(num1 ^ num2, (num1 & num2) << 1)

    def bitwise_subtraction(self, num1, num2):
        if num2 <= 0:
            return num1
        else:
            return self.bitwise_subtraction(num1 ^ num2, (~num1 & num2) << 1)

    def bitwise_multiplication(self, num1, num2):
        product = 0
        count = 0
        while num2 > 0:
            if num2 % 2 == 1:
                product += num1 << count
            count += 1
            num2 = num2 // 2
        return product

    def bitwise_division(self, num1, num2):
        sign = 1
        if num1 < 0 ^ num2 < 0:
            sign = -1
        # Make both nums positive
        num1 = abs(num1)
        num2 = abs(num2)
        quotient = 0
        temp = 0
        # test down from the highest bit and accumulate the tentative value for valid bit 
        for i in range(7, -1, -1): 
            if (temp + (num2 << i) <= num1): 
                temp += num2 << i 
                quotient |= 1 << i
        return sign * quotient

    def ALU_ADD(self, reg_a, reg_b):
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.bitwise_addition(self.MDR, self.REG[self.MAR])
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_ADDI(self, reg, value):
        self.MAR = value
        self.MDR = self.ram_read(value)
        self.MAR = reg
        self.MDR = self.bitwise_addition(self.REG[self.ram_read(self.MAR)], self.MDR)
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.ram_read(self.MAR)] = self.MDR

    def ALU_AND(self, reg_a, reg_b):
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.MDR & self.REG[self.MAR]
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_CMP(self, reg_a, reg_b):
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        self.MAR = self.ram_read(reg_a)
        if self.MDR > self.REG[self.MAR]:
            self.FL = 0b00000100 # reg a > reb b
        elif self.MDR == self.REG[self.MAR]:
            self.FL = 0b00000001 # they are equal
        else:
            self.FL = 0b00000010 # reg b > reb a

    def ALU_DEC(self, reg, unused):
        self.MAR = self.ram_read(reg)
        self.MDR = self.REG[self.MAR]
        self.MDR -= 1
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_INC(self, reg, unused):
        self.MAR = self.ram_read(reg)
        self.MDR = self.REG[self.MAR]
        self.MDR += 1
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_DIV(self, reg_a, reg_b):
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        if self.MDR == 0:
            print('Cannot divide by 0.')
            sys.exit(1)
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.bitwise_division(self.REG[self.MAR], self.MDR)
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_MOD(self, reg_a, reg_b):
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        if self.MDR == 0:
            print('Cannot MOD by 0.')
            sys.exit(1)
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.REG[self.MAR] % self.MDR # floor division?
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_MUL(self, reg_a, reg_b):
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.bitwise_multiplication(self.REG[self.MAR], self.MDR)
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_NOT(self, reg, unused):
        self.MAR = self.ram_read(reg)
        self.MDR = self.REG[self.MAR]
        self.MDR = ~self.MDR
        self.REG[self.MAR] = self.MDR

    def ALU_OR(self, reg_a, reg_b):
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.MDR | self.REG[self.MAR]
        self.REG[self.MAR] = self.MDR

    def ALU_SHL(self, reg_a, reg_b): # This is the same as multiplying a by 2**b.
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.REG[self.MAR] << self.MDR
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_SHR(self, reg_a, reg_b): # This is the same as floor dividing a by 2**b.
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.REG[self.MAR] >> self.MDR
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_SUB(self, reg_a, reg_b):
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.bitwise_subtraction(self.REG[self.MAR], self.MDR)
        self.MDR = self.MDR & 0xFF # keep values under maximum (255)
        self.REG[self.MAR] = self.MDR

    def ALU_XOR(self, reg_a, reg_b):
        self.MAR = self.ram_read(reg_b)
        self.MDR = self.REG[self.MAR]
        self.MAR = self.ram_read(reg_a)
        self.MDR = self.MDR ^ self.REG[self.MAR]
        self.REG[self.MAR] = self.MDR

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X %02X |" % (
            self.PC,
            self.FL,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.REG[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            if self.SP <= self.PC + 1:
                print('Stack overflow!')
                sys.exit(1)
            self.IR = self.ram_read(self.PC)
            if self.IR in self.instructions:
                num_operations = ((self.IR & 0b11000000) >> 6) + 1
                self.instructions[self.IR](num_operations)
            else:
                print(f'Unknown instruction {self.IR} at address {self.PC}')
                sys.exit(1)

    def handle_LDI(self, ops):
        self.MAR = self.ram_read(self.PC + 1)
        self.MDR = self.ram_read(self.PC + 2)
        self.REG[self.MAR] = self.MDR
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_LD(self, ops):
        self.MAR = self.REG[self.PC + 2]
        self.MDR = self.ram_read(self.MAR)
        self.MAR = self.PC + 1
        self.REG[self.MAR] = self.MDR

    def handle_PRN(self, ops):
        self.MAR = self.ram_read(self.PC + 1)
        print(self.REG[self.MAR])
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_PRA(self, ops):
        self.MAR = self.ram_read(self.PC + 1)
        self.MDR = self.REG[self.MAR]
        # convert ascii to character and print
        print(chr(self.MDR))
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_MUL(self, ops):
        self.alu('MUL', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_ADD(self, ops):
        self.alu('ADD', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_ADDI(self, ops):
        self.alu('ADDI', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_AND(self, ops):
        self.alu('AND', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_CALL(self, ops):
        self.MAR = self.bitwise_addition(self.PC, ops)
        # push address of next instruction to stack
        self.SP = self.bitwise_subtraction(self.SP, 1)
        if self.SP == self.PC:
            print(f'Stack overflow!')
            sys.exit(1)
        self.ram_write(self.MAR, self.SP)
        # set PC to address in given register
        self.MAR = self.ram_read(self.PC + 1)
        self.PC = self.REG[self.MAR]

    def handle_CMP(self, ops):
        self.alu('CMP', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_DEC(self, ops):
        self.alu('DEC', self.PC + 1, None)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_INC(self, ops):
        self.alu('INC', self.PC + 1, None)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_INT(self, ops):
        #get interrupt number from register
        self.MAR = self.PC + 1
        self.MDR = self.ram_read(self.MAR) # this is the reg number
        self.IS = self.REG[self.MDR]

    def handle_JEQ(self, ops):
        if self.FL == 1:
            self.MAR = self.ram_read(self.PC + 1)
            self.PC = self.REG[self.MAR]
        else:
            self.PC = self.bitwise_addition(self.PC, ops)

    def handle_JGE(self, ops):
        if self.FL == 2 or self.FL == 1:
            self.MAR = self.ram_read(self.PC + 1)
            self.PC = self.REG[self.MAR]
        else:
            self.PC = self.bitwise_addition(self.PC, ops)

    def handle_JGT(self, ops):
        if self.FL == 2:
            self.MAR = self.ram_read(self.PC + 1)
            self.PC = self.REG[self.MAR]
        else:
            self.PC = self.bitwise_addition(self.PC, ops)

    def handle_JLE(self, ops):
        if self.FL == 4 or self.FL == 1:
            self.MAR = self.ram_read(self.PC + 1)
            self.PC = self.REG[self.MAR]
        else:
            self.PC = self.bitwise_addition(self.PC, ops)

    def handle_JLT(self, ops):
        if self.FL == 4:
            self.MAR = self.ram_read(self.PC + 1)
            self.PC = self.REG[self.MAR]
        else:
            self.PC = self.bitwise_addition(self.PC, ops)

    def handle_JMP(self, ops):
        self.MAR = self.ram_read(self.PC + 1)
        self.PC = self.REG[self.MAR]

    def handle_JNE(self, ops):
        if self.FL != 1 and not 0:
            self.MAR = self.ram_read(self.PC + 1)
            self.PC = self.REG[self.MAR]
        else:
            self.PC = self.bitwise_addition(self.PC, ops)

    def handle_DIV(self, ops):
        self.alu('DIV', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_MOD(self, ops):
        self.alu('MOD', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_NOT(self, ops):
        self.alu('NOT', self.PC + 1, None)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_NOP(self, ops):
        # do nothing
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_OR(self, ops):
        self.alu('OR', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_POP(self, ops):
        # get value at current SP
        if self.SP == 0xF4:
            print('Stack is empty!')
            sys.exit(1)
        self.MAR = self.SP
        self.MDR = self.ram_read(self.MAR)
        self.MAR = self.PC + 1
        self.REG[self.ram_read(self.MAR)] = self.MDR
        # increment SP
        self.SP = self.bitwise_addition(self.SP, 1)
        # increment PC
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_PUSH(self, ops):
        # decrement Stack pointer
        self.SP = self.bitwise_subtraction(self.SP, 1)
        if self.SP <= self.PC + 1:
            print('Stack overflow!')
            sys.exit(1)
        # add value to stack
        self.MAR = self.ram_read(self.PC + 1)
        self.MDR = self.REG[self.MAR]
        self.ram_write(self.MDR, self.SP)
        # increment program counter
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_RET(self, ops):
        # Pop the value from the top of the stack and store it in the `PC`.
        if self.SP == 0xF4:
            print('Stack is empty!')
            sys.exit(1)
        self.PC = self.ram_read(self.SP)
        self.SP = self.bitwise_addition(self.SP, 1)

    def handle_SHL(self, ops):
        self.alu('SHL', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_SHR(self, ops):
        self.alu('SHR', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_ST(self, ops):
        # get value in register b
        self.MAR = self.PC + 2
        self.MDR = self.ram_read(self.MAR)
        self.MDR = self.REG[self.MDR]
        # get address from register a
        self.MAR = self.REG[self.PC + 1]
        self.ram_write(self.MDR, self.MAR)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_SUB(self, ops):
        self.alu('SUB', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_XOR(self, ops):
        self.alu('XOR', self.PC + 1, self.PC + 2)
        self.PC = self.bitwise_addition(self.PC, ops)

    def handle_HLT(self, ops):
        self.running = False
        self.PC = self.bitwise_addition(self.PC, ops)

    def ram_read(self, memory_address):
        return self.RAM[memory_address]

    def ram_write(self, memory_data, memory_address):
        self.RAM[memory_address] = memory_data
