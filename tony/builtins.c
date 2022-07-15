/*
  Built-in functions for Tony
*/
#include <stdio.h>
#include <string.h>

typedef int32_t integer;
typedef int8_t boolean;
typedef int8_t character;

void puti(integer n){
  printf("%d", n);
}

void putb(boolean b){
  b == 0 ? printf("false") : printf("true");
}

void putc(character c){
  printf("%c", c);
}

void puts(character* s){
  printf("%s", s);
}

integer geti(){
  integer n;
  scanf("%d", &n);
  return n;
}

boolean getb(){
  integer b;
  scanf("%d", &b);
  return (boolean) b;
}

character getc(){
  character c;
  scanf("%c", &c);
  return c;
}

character* gets(integer size, character *s){
  if( size <= 0 ){
    return NULL;
  }

  character buffer[size];
  memset(bufffer, 0, size);

  int bytes_read = 0;
  character c;

  while(bytes_read <= size-1){ // reserving one byte for \0
    c = getchar();
    if (c == EOF || c == '\n') break;
    buffer[bytes_read++] = c;
  }

  strcpy((char *) s, (char *) buffer);
}
