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
        self.FL = [0] * 8
        self.running = False
        self.instructions = {}
        self.instructions[0b10000010] = self.handle_LDI
        self.instructions[0b01000111] = self.handle_PRN
        self.instructions[0b10100010] = self.handle_MUL
        self.instructions[0b10100000] = self.handle_ADD
        self.instructions[0b00000001] = self.handle_HLT

    def load(self):
        """Load a program into memory."""

        self.MAR = 0

        program = sys.argv[1]

        with open(program) as file:
            for line in file:
                # if the line is a line break or a comment, don't add to memory
                if line[0] is '#' or line[0] is '\n':
                    continue
                self.MDR = int(line[:8], 2) # only read the command code
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

        if op == "ADD":
            # self.REG[reg_a] += self.REG[reg_b]
            self.MAR = self.ram_read(reg_b)
            self.MDR = self.REG[self.MAR]
            self.MAR = self.ram_read(reg_a)
            self.MDR = self.MDR + self.REG[self.MAR]
            self.REG[self.MAR] = self.MDR
        elif op == "MUL":
            # self.REG[reg_a] = self.REG[reg_a] * self.REG[reg_b]
            self.MAR = self.ram_read(reg_b)
            self.MDR = self.REG[self.MAR]
            self.MAR = self.ram_read(reg_a)
            self.MDR = self.MDR * self.REG[self.MAR]
            self.REG[self.MAR] = self.MDR
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
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
            self.IR = self.ram_read(self.PC)
            if self.IR in self.instructions:
                self.instructions[self.IR]()
            else:
                print(f'Unknown instruction {self.IR} at address {self.PC}')
                sys.exit(1)

    def handle_LDI(self):
        self.MAR = self.ram_read(self.PC + 1)
        self.MDR = self.ram_read(self.PC + 2)
        self.REG[self.MAR] = self.MDR
        self.PC += 3

    def handle_PRN(self):
        self.MAR = self.ram_read(self.PC + 1)
        print(self.REG[self.MAR])
        self.PC += 2

    def handle_MUL(self):
        self.alu('MUL', self.PC + 1, self.PC + 2)
        self.PC += 3

    def handle_ADD(self):
        self.alu('ADD', self.PC + 1, self.PC + 2)
        self.PC += 3

    def handle_HLT(self):
        self.running = False
        self.PC += 1

    def ram_read(self, memory_address):
        return self.RAM[memory_address]

    def ram_write(self, memory_data, memory_address):
        self.RAM[memory_address] = memory_data
