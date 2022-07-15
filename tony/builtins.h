#ifndef builtins_h_
#define builtins_h_

// Output
extern void puti(integer);
extern void putb(boolean);
extern void putc(character);
extern void puts(character*);

// Input
extern integer   geti();
extern boolean   getb();
extern character getc();
extern void      gets(integer, character*);

// Conversions
extern integer   abs(integer);
extern integer   ord(character);
extern character chr(integer);

// String functions
extern integer strlen(character*)
extern integer strcmp(character*, character*)
extern void    strcpy(character*, character*)
extern void    strcat(character*, character*)

#endif
