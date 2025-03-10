#include <stdio.h>
#include <stdlib.h>

int main(){
    scanf();

}
#define MAX_BOOKS 100
#define TITLE_LENGTH 50

typedef struct {
    char title[TITLE_LENGTH];
    char author[TITLE_LENGTH];
    int year;
} Book;

void addBook(Book library[], int *bookCount) {
    if (*bookCount >= MAX_BOOKS) {
        printf("Library is full!\n");
        return;
    }
    printf("Enter title: ");
    scanf(" %[^\n]", library[*bookCount].title);
    printf("Enter author: ");
    scanf(" %[^\n]", library[*bookCount].author);
    printf("Enter year: ");
    scanf("%d", &library[*bookCount].year);
    (*bookCount)++;
}

void listBooks(Book library[], int bookCount) {
    for (int i = 0; i < bookCount; i++) {
        printf("Book %d: %s by %s, %d\n", i + 1, library[i].title, library[i].author, library[i].year);
    }
}

int main() {
    Book library[MAX_BOOKS];
    int bookCount = 0;
    int choice;

    while (1) {
        printf("1. Add book\n");
        printf("2. List books\n");
        printf("3. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                addBook(library, &bookCount);
                break;
            case 2:
                listBooks(library, bookCount);
                break;
            case 3:
                exit(0);
            default:
                printf("Invalid choice!\n");
        }
    }

    return 0;
}