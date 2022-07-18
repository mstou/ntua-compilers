/*
  Built-in functions for Tony
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef int32_t integer;
typedef int8_t boolean;
typedef int8_t character;

void _puti(integer n) {
  printf("%d", n);
}

void _putb(boolean b) {
  b == 0 ? printf("false") : printf("true");
}

void _putc(character c) {
  printf("%c", c);
}

void _puts(character* s) {
  printf("%s", (char *) s);
}

integer _geti() {
  integer n;
  scanf("%d", &n);
  return n;
}

boolean _getb() {
  integer b;
  scanf("%d", &b);
  return (boolean) b;
}

character _getc() {
  character c;
  scanf("%c", &c);
  return c;
}

void _gets(integer size, character *s) {
  if( size <= 0 ){
    return;
  }

  character buffer[size];
  memset(buffer, 0, size);

  int bytes_read = 0;
  character c;

  while(bytes_read <= size-1) { // reserving one byte for \0
    c = getchar();
    if (c == EOF || c == '\n') break;
    buffer[bytes_read++] = c;
  }

  strcpy((char *) s, (char *) buffer);
}

integer _abs(integer n) {
  return abs(n);
}

integer _ord(character c) {
  return (integer) c;
}

character _chr(integer n) {
  return (character) n;
}

integer _strlen(character* s) {
  return strlen((char *) s);
}

integer _strcmp(character* s1, character* s2) {
  return strcmp((char *) s1, (char *) s2);
}

void _strcpy(character* s1, character* s2) {
  strcpy((char *) s1, (char *) s2);
}

void _strcat(character* s1, character* s2) {
  strcat((char *) s1, (char *) s2);
}
