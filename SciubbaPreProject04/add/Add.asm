// This file is modeled off of a program described in
// the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/add/Add.asm

// Adds two constants (2 and 3) and writes their sum to RAM[0]

    // performs the addition
    @2
    D=A
    @3
    D=D+A

    // stores the value in R0
    @R0
    M=D
(END)
    @END
    0;JMP