// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.
   
    @n
    M=0         // n = 0 

    @R2
    M=0         //R2 = 0

(LOOP)
    
    @R0
    D=M
    @R2
    M=D+M       // R2 += R0
    
    @n
    DM=M+1
    @R1
    D=D-M
    @LOOP
    D;JLT       // if (n != R1) repeat

(END)
    
    @END
    0;JMP       //goto END