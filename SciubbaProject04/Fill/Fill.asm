// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

(WAIT)          // determines if screen should be white or black
    @n
    M=0

    @color 
    M=-1
    @KBD
    D=M
    @LOOP
    D;JNE       // if (KBD != 0) goto LOOP with color = -1

    
    @color
    M=0
    @LOOP
    0;JMP       // else goto LOOP with color = 0
(LOOP)
    
    @n
    D=M
    @8192
    D=D-A
    @WAIT
    D;JEQ       // if (n == 8192) goto WAIT

    
    @n
    D=M
    @SCREEN
    D=D+A
    @R0
    M=D
    @color
    D=M
    @R0
    A=M
    M=D         // sets the next 16 pixels to the value stored in color

    
    @n
    M=M+1       // n = n + 1

    
    @LOOP
    0;JMP       // goto LOOP
