#ifndef _H_HPP
#define _H_HPP

#include <iostream>
#include <cstdlib>
#include <cstring>
#include <cassert>
#include <map>
using namespace std;

								// ********************** Virtual FORTH Machine
								// configuration
#define Msz 0x1000
#define Rsz 0x100
#define Dsz 0x10
								// machine word size
#define CELL sizeof(int32_t)

extern uint8_t M[Msz];			// memory
extern uint32_t Ip;				// instruction pointer
extern uint32_t Cp;				// compilation pointer (free heap begin)

#define _entry  1				// program entry point (addr of jmp parameter)
#define _latest (_entry+CELL)	// last defined word LFA address

extern void dump();				// dump M[] to bin.bin file

extern void set(uint32_t addr, int32_t value);	// set cell in M[] byte by byte
extern uint32_t get(uint32_t addr);				// get cell from M[]

extern void Cbyte( uint8_t);	// compile byte
extern void Ccell(uint32_t);	// compile cell
extern void Cstring(char*);		// compile ASCIIZ string

								// === compile vocabulary header for new word
extern void Cheader(char*s);
extern void LFA();				// Link Field Area pointer of previous word
extern void AFA(uint8_t b=0);	// Attrubute Field Area (IMMEDIATE flag)
extern void NFA(char*);			// Name Field Area (ASCIIZ string, word name)
extern void CFA(string);		// Code Field Area (compiled bytecode)
extern void PFA();				// Parameter Field Area (for var/const values)

extern map<string,uint32_t> SymTable;	// compiler symbol table

extern uint32_t R[Rsz];			// \ return stack
extern uint32_t Rp;				// /

extern  int32_t D[Dsz];			// \ data stack
extern uint32_t Dp;				// /

								// ==== bytecode commands ====
#define opNOP	0x00	// nop
#define opBYE	0xFF	// bye
#define opJMP	0x01	// jmp <addr>
#define opQJMP	0x02	// ?jmp <addr>
#define opCALL	0x03	// call <addr>
#define opRET	0x04	// ret
#define opLIT	0x05	// lit <value>

extern void VM();				// bytecode interpreter

								// lexer/parser interface for bytecode compiler
extern int yylex();
extern int yylineno;
extern char* yytext;
extern int yyparse();
extern void yyerror(string);
#include "ypp.tab.hpp"

#endif // _H_HPP
