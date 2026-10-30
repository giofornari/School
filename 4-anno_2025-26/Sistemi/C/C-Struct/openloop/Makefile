# Makefile per openloop
CC = gcc
CFLAGS = -Wall -Wextra -std=c11 -g
TARGET = openloop
BINDIR = bin
OBJDIR = obj
SRCDIR = src
INCDIR = include

# File sorgenti e oggetti
SOURCES = $(wildcard $(SRCDIR)/*.c)
OBJECTS = $(patsubst $(SRCDIR)/%.c,$(OBJDIR)/%.o,$(SOURCES))

# Target principale
$(BINDIR)/$(TARGET): $(OBJECTS) | $(BINDIR)
	$(CC) $(CFLAGS) $^ -o $@
	@echo "Compilazione completata: $(BINDIR)/$(TARGET)"

# Regola per compilare i file oggetto
$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
	$(CC) $(CFLAGS) -I$(INCDIR) -c $< -o $@

# Crea le directory se non esistono
$(BINDIR):
	mkdir -p $(BINDIR)

$(OBJDIR):
	mkdir -p $(OBJDIR)

# Target per eseguire il programma
run: $(BINDIR)/$(TARGET)
	./$(BINDIR)/$(TARGET)

# Pulizia
clean:
	rm -rf $(OBJDIR) $(BINDIR)
	@echo "Pulizia completata"

# Rebuild completo
rebuild: clean $(BINDIR)/$(TARGET)

.PHONY: clean run rebuild
