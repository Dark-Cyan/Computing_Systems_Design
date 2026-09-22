// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/rect/Rect.asm

// Draw a rectangle of RAM[0] rows of 16 pixels each on the screen. 
// The rectangle’s top-left corner is located at the top-left corner 
// of the screen.

// Test code makes a rectangle that is half the height of the screen

    @n
    M=0

    @32
    D=A
    @row
    M=D

    @currentRow
    M=0
(LOOP)
    // if (n == RAM[0]) goto END
    @n
    D=M
    @R0
    D=D-M
    @END
    D;JEQ

    // Sets the first 16 pixels of the current row to black
    @currentRow
    D=M
    @SCREEN
    A=D+A
    M=-1

    // n = n + 1
    @n
    M=M+1

    // currentRow += 32 ~ goes to next row
    @row
    D=M
    @currentRow
    M=D+M

    // goto LOOP
    @LOOP
    0;JMP
(END)
    @END
    0;JMP

    
