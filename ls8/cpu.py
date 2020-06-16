"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.MAR = 0 # Memory Address Register
        self.MDR = 0 # Memory Data Register

    def load(self):
        """Load a program into memory."""

        self.MAR = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        while self.MAR < len(program):
            self.MDR = program[self.MAR]
            self.ram_write(self.MDR, self.MAR)
            self.MAR += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            instruction_register = self.ram_read(self.pc)
            if instruction_register == 0b10000010: # LDI load immediate
                self.MAR = self.ram_read(self.pc + 1)
                self.MDR = self.ram_read(self.pc + 2)
                self.reg[self.MAR] = self.MDR
                self.pc += 3
            elif instruction_register == 0b01000111: # PRN print register
                self.MAR = self.ram_read(self.pc + 1)
                print(self.reg[self.MAR])
                self.pc += 2
            elif instruction_register == 0b00000001: # HLT halt
                running = False
                self.pc += 1
            else:
                print(f'Unknown instruction {instruction_register} at address {self.pc}')
                sys.exit(1)


    def ram_read(self, memory_address):
        return self.ram[memory_address]

    def ram_write(self, memory_data, memory_address):
        self.ram[memory_address] = memory_data
