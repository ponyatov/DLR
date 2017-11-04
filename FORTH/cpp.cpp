#include "hpp.hpp"
#define YYERR "\n\n"<<yylineno<<":"<<msg<<"["<<yytext<<"]\n\n"
void yyerror(string msg) { cout<<YYERR; cerr<<YYERR; exit(-1); }

int main(int argc, char *argv[]) {
	// compile vocabulary header
	Cbyte(opJMP); Ccell(0);			// jmp _entry	jump to last defined word
	Ccell(0);						// _latest		LFA of last defined word
	// run compiler
	yyparse();
	// dump memory
	dump();
	// run VM
	VM();
	return 0;
}

// ****************************************************** Virtual FORTH Machine

// ===================================================================== stacks

uint32_t R[Rsz];			// \ return stack
uint32_t Rp;				// /

 int32_t D[Dsz];			// \ data stack
uint32_t Dp;				// /

// ===================================================================== memory

uint8_t M[Msz];			// memory
uint32_t Ip=0;			// instruction pointer
uint32_t Cp=0;			// compilation pointer (free heap begin)

void set(uint32_t addr, int32_t value) {
	assert(addr+3<Msz);
	M[addr+0] = (value>>0x00) & 0xFF;
	M[addr+1] = (value>>0x08) & 0xFF;
	M[addr+2] = (value>>0x10) & 0xFF;
	M[addr+3] = (value>>0x18) & 0xFF;	}

uint32_t get(uint32_t addr) {
	assert(addr+3<Msz);
	return \
		M[addr+0]<<0x00 | M[addr+1]<<0x08 | \
		M[addr+2]<<0x10 | M[addr+3]<<0x18;	}

// =================================================================== compiler

void Cbyte( uint8_t b) { M[Cp++] = b; assert(Cp<Msz); }
void Ccell(uint32_t b) { set(Cp,b); Cp+= CELL; assert(Cp<Msz); }
void Cstring(char* s) {
	uint32_t L = strlen(s); assert(Cp+L+1<Msz);
	memcpy(&M[Cp],s,L+1); Cp += L+1; }

void dump() {
	FILE *img = fopen("bin.bin","wb"); assert(img);
	assert(fwrite(M,1,Cp,img)==Cp);
	fclose(img);
}

map<string,uint32_t> SymTable;								// symbol table

void LFA() { uint32_t L = get(_latest); set(_latest,Cp); Ccell(L); }
void AFA(uint8_t b) { Cbyte(b); }
void NFA(char* s) { Cstring(s); }
void CFA(string s) { SymTable[s] = Cp; set(_entry,Cp); }
void Cheader(char*s) { LFA(); AFA(); NFA(s); CFA(s); }

// ======================================================= bytecode interpreter

void nop() { printf("nop"); }
void bye() { printf("bye\n\n"); exit(0); }
void jmp() { printf("jmp "); Ip=get(Ip); assert(Ip<=Cp); printf("%.4X",Ip); }
void call() {
	printf("call "); assert(Rp < Rsz); R[Rp++] = Ip+CELL;
	Ip = get(Ip); assert(Ip <= Cp); }
void ret() { printf("ret"); assert(Rp>0); Ip=R[--Rp]; assert(Ip<=Cp); }
void lit() {
	printf("lit "); assert(Dp < Dsz);
	D[Dp++] = get(Ip); printf("%.4X", D[Dp - 1]);
	Ip += CELL; assert(Ip <= Cp); }

void VM() { for (;;) {
	printf("%.4X ",Ip);
	uint8_t op = M[Ip++]; assert(Ip<=Cp);	// FETCH
	printf("%.2X ",op);
	switch (op) {							// DECODE/EXECUTE
		case opNOP : nop();  break;
		case opBYE : bye();  break;
		case opJMP : jmp();  break;
		case opCALL: call(); break;
		case opRET : ret();  break;
		case opLIT : lit();  break;
		default:
			printf("bad opcode\n\n"); abort();
	}
	printf("\n");
}}
