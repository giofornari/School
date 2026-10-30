# Makefile for safe_copy project
# Author: giordii (admin@giordii.dev)
# Date: 2025-12-04

CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -pedantic -g
TARGET = safe_copy
BINDIR = bin
SRCDIR = src
INCDIR = include
OBJDIR = obj

# Source files
SOURCES = $(SRCDIR)/main.c $(SRCDIR)/utils.c
OBJECTS = $(OBJDIR)/main.o $(OBJDIR)/utils.o

# Main target
all: directories $(BINDIR)/$(TARGET)

# Create necessary directories
directories:
	@mkdir -p $(BINDIR)
	@mkdir -p $(OBJDIR)

# Link object files to create executable
$(BINDIR)/$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $(OBJECTS)
	@echo "Compilazione completata: $(BINDIR)/$(TARGET)"

# Compile source files to object files
$(OBJDIR)/main.o: $(SRCDIR)/main.c $(INCDIR)/utils.h
	$(CC) $(CFLAGS) -c $< -o $@

$(OBJDIR)/utils.o: $(SRCDIR)/utils.c $(INCDIR)/utils.h
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -rf $(BINDIR) $(OBJDIR)
	@echo "Pulizia completata"

# Run the program with test files
test: all
	@echo "\n=== Test 1: Copia normale ==="
	@echo "Contenuto di test" > test_input.txt
	./$(BINDIR)/$(TARGET) test_input.txt test_output.txt
	@echo "\n=== Test 2: File sorgente inesistente ==="
	./$(BINDIR)/$(TARGET) file_inesistente.txt output.txt 2>err.log || true
	@echo "\n=== Contenuto err.log ==="
	@cat err.log
	@rm -f test_input.txt test_output.txt err.log

# Install (copy to user bin - optional)
install: all
	@echo "Per installare il programma, esegui:"
	@echo "sudo cp $(BINDIR)/$(TARGET) /usr/local/bin/"

.PHONY: all clean test directories install
