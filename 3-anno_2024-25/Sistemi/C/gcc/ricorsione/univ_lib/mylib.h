#ifndef MYLIB_H
#define MYLIB_H

#include <stdio.h>
#include <string.h>

#define MAX 100
#define MAX_DIM 1000

int cerca(int num[], int left, int right, int target);
void gira(char *x, char *y);
void permute(char str[], int left, int right);
void stampaNumeri(int n);
void printArray(int n[], int dim);
int sommaNum(int num);
long long int sommaCifre(long long n);
int contrPar(int i[], int dim);
int ctrlPalidr(char s[], int start, int end);
int cercaMin(int n[], int dim);
void convBin(int n);

#endif // MYLIB_H
