#ifndef MYNETLIB_H
#define MYNETLIB_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* ipToBinary(const char* ip_input);

void generateHostAddresses(const char* networkIp, int cidr);

int isValidIPv4(char* ip);

void calculateNetworkAddress(char* ip, int cidr);

#endif // MYNETLIB_H