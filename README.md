Nicholas Lee
Dr. Peter Crawshaw
COMP3971
March 2023

Assignment 3 Design Document

For this assignment, I decided to use Python to implement my disassembler This uses the C Struct library for parsing byte objects where necessary.

The main function is used to take in a filename from the user, check that the file exists, and disassemble the data from that file. This repeats until the user states they no longer wish to process any more files.

The disassemble function, takes a filename and opens it to read binary. First we seek the header information for the .text and .data segments. For this assignment all we need is the size and offset of these segments Once we have this information, we loop through each instruction (every 4 bytes after the offset) and send them to the disassemble_instruction function. Here is where we print out each disassembled instruction. We then do the same for the .data segment where we only print out the hex value for each 4 bytes after the offset.

The disassemble_instruction function takes in a 32-bit binary RISC-V instruction and decodes it according to its opcode/funct values and returns the proper format depending on its type. This is only applicable to the instructions stated in the assignment handout but could be updated to read any instruction necessary.
