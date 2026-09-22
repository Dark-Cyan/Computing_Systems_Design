// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/rect/Rect.tst

load Rect.asm;
echo "Make sure that 'No Animation' is selected.";

set RAM[0] 128;

repeat {
  ticktock;
}
