#ifndef OKFGEN_LINKED_LIST_H
#define OKFGEN_LINKED_LIST_H

/** @brief A node in a singly-linked list holding an integer value. */
typedef struct Node {
    int data;
    struct Node* next;
} Node;

/** @brief Opaque linked list handle. */
typedef struct {
    Node* head;
    int size;
} LinkedList;

/** @brief Create a new empty linked list. Returns NULL on allocation failure. */
LinkedList* list_create(void);

/** @brief Insert a value at the front of the list. Returns 0 on success. */
int list_push_front(LinkedList* list, int value);

/** @brief Insert a value at the back of the list. Returns 0 on success. */
int list_push_back(LinkedList* list, int value);

/** @brief Remove and return the first element. Returns 0 if the list is empty. */
int list_pop_front(LinkedList* list);

/** @brief Remove the first occurrence of value. Returns 0 if found, -1 if not. */
int list_remove(LinkedList* list, int value);

/** @brief Traverse the list, calling visit for each element. */
void list_traverse(const LinkedList* list, void (*visit)(int));

/** @brief Return the number of elements in the list. */
int list_size(const LinkedList* list);

/** @brief Free all memory used by the list. */
void list_destroy(LinkedList* list);

#endif /* OKFGEN_LINKED_LIST_H */
