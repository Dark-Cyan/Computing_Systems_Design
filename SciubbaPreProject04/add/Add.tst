load Add.asm,
output-file Add.out,
compare-to Add.cmp,
output-list RAM[0]%D2.6.2;

repeat 20 {
  ticktock;
}

output;