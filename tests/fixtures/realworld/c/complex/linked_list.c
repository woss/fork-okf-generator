#include "linked_list.h"
#include <stdlib.h>

LinkedList* list_create(void) {
    LinkedList* list = (LinkedList*)malloc(sizeof(LinkedList));
    if (!list) return NULL;
    list->head = NULL;
    list->size = 0;
    return list;
}

static Node* node_create(int value) {
    Node* node = (Node*)malloc(sizeof(Node));
    if (!node) return NULL;
    node->data = value;
    node->next = NULL;
    return node;
}

int list_push_front(LinkedList* list, int value) {
    Node* node = node_create(value);
    if (!node) return -1;
    node->next = list->head;
    list->head = node;
    list->size++;
    return 0;
}

int list_push_back(LinkedList* list, int value) {
    Node* node = node_create(value);
    if (!node) return -1;
    if (!list->head) {
        list->head = node;
    } else {
        Node* cur = list->head;
        while (cur->next) cur = cur->next;
        cur->next = node;
    }
    list->size++;
    return 0;
}

int list_pop_front(LinkedList* list) {
    if (!list->head) return 0;
    Node* old = list->head;
    int value = old->data;
    list->head = old->next;
    free(old);
    list->size--;
    return value;
}

int list_remove(LinkedList* list, int value) {
    Node *cur = list->head, *prev = NULL;
    while (cur) {
        if (cur->data == value) {
            if (prev) prev->next = cur->next;
            else list->head = cur->next;
            free(cur);
            list->size--;
            return 0;
        }
        prev = cur;
        cur = cur->next;
    }
    return -1;
}

void list_traverse(const LinkedList* list, void (*visit)(int)) {
    Node* cur = list->head;
    while (cur) {
        visit(cur->data);
        cur = cur->next;
    }
}

int list_size(const LinkedList* list) {
    return list->size;
}

void list_destroy(LinkedList* list) {
    Node* cur = list->head;
    while (cur) {
        Node* next = cur->next;
        free(cur);
        cur = next;
    }
    free(list);
}
