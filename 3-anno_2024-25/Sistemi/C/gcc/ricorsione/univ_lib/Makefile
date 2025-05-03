CC = gcc
CFLAGS = -Wall -Wextra

all: recursive_demo

recursive_demo: main.o mylib.o
	$(CC) $(CFLAGS) -o recursive_demo main.o mylib.o

main.o: main.c mylib.h
	$(CC) $(CFLAGS) -c main.c

mylib.o: mylib.c mylib.h
	$(CC) $(CFLAGS) -c mylib.c

clean:
	rm -f *.o recursive_demo
