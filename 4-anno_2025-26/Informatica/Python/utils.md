```py
import ciao
# bla
```

# Giordi

## Dictionary

## List

Di seguito sono elencati i metodi principali che possono essere utilizzati sulle liste.

| Metodo             | Descrizione                                                                                                |
| ------------------ | ---------------------------------------------------------------------------------------------------------- |
| `append()`         | Aggiunge un elemento alla fine della lista.                                                                |
| `clear()`          | Rimuove tutti gli elementi dalla lista.                                                                    |
| `copy()`           | Restituisce una copia della lista.                                                                         |
| `count(x)`         | Restituisce il numero di volte in cui `x` appare nella lista.                                              |
| `extend(iterable)` | Aggiunge gli elementi di un'altra lista (o di un qualsiasi iterabile) alla lista corrente.                 |
| `index(x)`         | Restituisce l'indice della prima occorrenza dell'elemento `x`.                                             |
| `insert(i, x)`     | Inserisce l'elemento `x` in posizione `i`.                                                                 |
| `pop(i)`           | Rimuove e restituisce l'elemento nella posizione `i`. Se `i` non è specificato, rimuove l'ultimo elemento. |
| `remove(x)`        | Rimuove la prima occorrenza dell'elemento `x`.                                                             |
| `reverse()`        | Inverte l'ordine degli elementi nella lista.                                                               |
| `sort()`           | Ordina la lista in ordine crescente (modificabile con parametri).                                          |

---

### 🔍 Esempi Pratici

### 1️⃣ **Aggiungere un elemento alla fine della lista**

```python
fruits = ["mela", "banana", "ciliegia"]
fruits.append("arancia")
print(fruits)  # Output: ['mela', 'banana', 'ciliegia', 'arancia']
```

### 2️⃣ **Rimuovere un elemento specifico**

```python
numbers = [1, 2, 3, 4, 5]
numbers.remove(3)
print(numbers)  # Output: [1, 2, 4, 5]
```

### 3️⃣ **Ordinare una lista**

```python
nums = [4, 2, 9, 1]
nums.sort()
print(nums)  # Output: [1, 2, 4, 9]
```

### 4️⃣ **Invertire l'ordine di una lista**

```python
letters = ['a', 'b', 'c']
letters.reverse()
print(letters)  # Output: ['c', 'b', 'a']
```

## Array

Gli **array** vengono gestiti con il modulo `array`, che permette di definire array con un tipo di dato specifico.

### 📋 **Metodi principali degli Array**
| Metodo         | Descrizione |
|---------------|------------|
| `append(x)`   | Aggiunge un elemento alla fine dell'array. |
| `extend(iterable)` | Aggiunge più elementi da un iterabile. |
| `insert(i, x)` | Inserisce un elemento `x` nella posizione `i`. |
| `remove(x)`   | Rimuove la prima occorrenza dell'elemento `x`. |
| `pop(i)`      | Rimuove e restituisce l'elemento in posizione `i` (se non specificato, rimuove l'ultimo). |
| `index(x)`    | Restituisce l'indice della prima occorrenza di `x`. |
| `count(x)`    | Conta quante volte `x` appare nell'array. |
| `reverse()`   | Inverte l'ordine degli elementi nell'array. |
| `tolist()`    | Converte l'array in una lista. |

### 🔍 **Esempio di utilizzo degli Array**
```python
import array

# Creazione di un array di interi
arr = array.array('i', [1, 2, 3, 4])
arr.append(5)
arr.remove(2)

print(arr)  # Output: array('i', [1, 3, 4, 5])
```

## Tuples

## Other stuffs
