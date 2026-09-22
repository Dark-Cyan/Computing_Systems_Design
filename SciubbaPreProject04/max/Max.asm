// This file is modeled off of a program described in
// the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Aill.asm

// Computes the maximum of RAM[0] and RAM[1] and writes the result in RAM[2]

// if (R0 > R1) goto FIRST
    @R0
    D=M
    @R1
    D=D-M
    @FIRST
    D;JGT

// else goto SECOND
    @SECOND
    0;JMP
(FIRST)
    // R2 = R0
    @R0
    D=M
    @R2
    M=D
    @END
    0;JMP
(SECOND)
    // R2 = R1
    @R1
    D=M
    @R2
    M=D
    @END
    0;JMP
(END)
    @END
    0;JMP

    
