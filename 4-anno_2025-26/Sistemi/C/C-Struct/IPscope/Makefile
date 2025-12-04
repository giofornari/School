# Makefile per il progetto randip
# 
# Questo Makefile compila un progetto C modulare con:
# - Separazione tra header e sorgenti
# - Compilazione separata dei moduli
# - Linking finale
# - Target per pulizia e rebuild

# === CONFIGURAZIONE COMPILATORE ===

# Compilatore C
CC = gcc

# Flag di compilazione
# -Wall: abilita tutti i warning comuni
# -Wextra: abilita warning extra
# -std=c11: usa lo standard C11
# -g: include informazioni di debug per gdb/valgrind
# -O2: ottimizzazione livello 2 (bilanciamento velocità/dimensione)
CFLAGS = -Wall -Wextra -std=c11 -g -O2

# Directory
SRC_DIR = src
INC_DIR = include
OBJ_DIR = obj
BIN_DIR = bin

# Include path
INCLUDES = -I$(INC_DIR)

# Nome dell'eseguibile
TARGET = $(BIN_DIR)/randip

# === FILE DEL PROGETTO ===

# Tutti i file .c nella directory src
SOURCES = $(wildcard $(SRC_DIR)/*.c)

# Trasforma i .c in .o nella directory obj
# Esempio: src/main.c -> obj/main.o
OBJECTS = $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(SOURCES))

# Header files (per dependency tracking)
HEADERS = $(wildcard $(INC_DIR)/*.h)

# === TARGET PRINCIPALI ===

# Target di default: compila tutto
all: directories $(TARGET)

# Crea le directory necessarie se non esistono
directories:
	@mkdir -p $(OBJ_DIR)
	@mkdir -p $(BIN_DIR)

# Link: combina tutti gli object file nell'eseguibile
$(TARGET): $(OBJECTS)
	@echo "Linking $@..."
	$(CC) $(CFLAGS) $(OBJECTS) -o $(TARGET)
	@echo "Build completata: $(TARGET)"

# Compilazione: compila ogni .c in .o
# $< = primo prerequisito (il file .c)
# $@ = target (il file .o)
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c $(HEADERS)
	@echo "Compilazione $<..."
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# === TARGET DI UTILITÀ ===

# Pulizia: rimuove file compilati
clean:
	@echo "Pulizia file compilati..."
	rm -rf $(OBJ_DIR)
	rm -f $(TARGET)
	@echo "Pulizia completata"

# Pulizia completa: rimuove anche le directory
distclean: clean
	rm -rf $(BIN_DIR)

# Rebuild: pulisci e ricompila tutto
rebuild: clean all

# Esegui il programma con un esempio
run: $(TARGET)
	@echo "Esecuzione di randip..."
	@echo ""
	./$(TARGET) -n 5

# Test con vari parametri
test: $(TARGET)
	@echo "=== Test 1: IP singolo ==="
	./$(TARGET)
	@echo ""
	@echo "=== Test 2: 5 IP casuali ==="
	./$(TARGET) -n 5
	@echo ""
	@echo "=== Test 3: 5 IP classe A ==="
	./$(TARGET) -n 5 -c A
	@echo ""
	@echo "=== Test 4: 5 IP in subnet ==="
	./$(TARGET) -n 5 -i 192.168.1.0/24
	@echo ""
	@echo "=== Test 5: Help ==="
	./$(TARGET) -h

# Verifica memory leak con valgrind
memcheck: $(TARGET)
	@echo "Controllo memory leak con valgrind..."
	valgrind --leak-check=full --show-leak-kinds=all \
		--track-origins=yes --verbose \
		./$(TARGET) -n 100

# Debug con gdb
debug: $(TARGET)
	gdb --args $(TARGET) -n 5 -c A

# Analisi statica del codice
analyze:
	@echo "Analisi statica del codice..."
	cppcheck --enable=all --suppress=missingIncludeSystem $(SRC_DIR)

# Stampa informazioni sul progetto
info:
	@echo "=== Informazioni Progetto randip ==="
	@echo "Compilatore: $(CC)"
	@echo "Flags: $(CFLAGS)"
	@echo "Sorgenti: $(SOURCES)"
	@echo "Objects: $(OBJECTS)"
	@echo "Headers: $(HEADERS)"
	@echo "Target: $(TARGET)"

# Installa il programma (richiede privilegi root)
install: $(TARGET)
	@echo "Installazione di randip in /usr/local/bin..."
	sudo cp $(TARGET) /usr/local/bin/
	@echo "Installazione completata"

# Disinstalla il programma
uninstall:
	@echo "Rimozione di randip da /usr/local/bin..."
	sudo rm -f /usr/local/bin/randip
	@echo "Disinstallazione completata"

# === DOCUMENTAZIONE ===

# Genera documentazione con Doxygen (se disponibile)
docs:
	@if command -v doxygen > /dev/null; then \
		echo "Generazione documentazione con Doxygen..."; \
		doxygen Doxyfile; \
	else \
		echo "Doxygen non trovato. Installalo per generare la documentazione."; \
	fi

# === PHONY TARGETS ===

# Dichiara i target che non sono file reali
.PHONY: all clean distclean rebuild run test memcheck debug analyze info \
        install uninstall docs directories

# === NOTE SUL MAKEFILE ===

# Pattern Rules:
# $(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
#   Dice: per creare un .o, compila il corrispondente .c
#   % è un wildcard che matcha qualsiasi stringa

# Automatic Variables:
# $@ = nome del target
# $< = primo prerequisito
# $^ = tutti i prerequisiti
# $* = stem (parte che matcha %)

# Esempio di esecuzione:
# make              -> compila tutto
# make clean        -> rimuove file compilati
# make rebuild      -> pulisce e ricompila
# make run          -> compila ed esegue
# make test         -> esegue test automatici
# make memcheck     -> controlla memory leak
# make install      -> installa il programma

# Dipendenze automatiche:
# Ogni .o dipende dal suo .c e da tutti gli header
# Se modifichi un header, tutti i moduli vengono ricompilati
# (Approccio semplificato; per progetti grandi usare gcc -MMD)

# Compilazione incrementale:
# Make compila solo i file modificati
# Controlla i timestamp per determinare cosa ricompilare
