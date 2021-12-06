#include <iostream>
#include <unordered_map>
#include <algorithm>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <fstream>
using namespace std;

class LRUCache {
    struct LinkedList {
        int key; 

        LinkedList* next;
        LinkedList* prev;
        
        LinkedList (): key(-1), prev(nullptr), next(nullptr) {}
        LinkedList (int _key): key(_key), prev(nullptr), next(nullptr) {}
    };

    int capacity_, size_;
    unordered_map<int, LinkedList*> hashMap;
    
    LinkedList* head;
    LinkedList* tail;

    int page_fault_num;

public:
    LRUCache(int capacity) {
        head = new LinkedList();
        tail = new LinkedList();

        head -> next = tail;
        tail -> prev = head;
        capacity_ = capacity;
        size_ = 0;

        page_fault_num = 0;
    }

    void put(int key) {
        if (hashMap.find(key) == hashMap.end()) {
            LinkedList* node = new LinkedList(key);
            hashMap[key] = node;
            addNodeToHead(node);
            size_++;
            if (size_ > capacity_) {
                LinkedList* removedNode = removeTailNode();
                hashMap.erase(removedNode -> key);
                delete removedNode;
                size_--;
                page_fault_num++;
            }
        }
        else {
            LinkedList* node = hashMap[key];
            moveNodeToHead(node);
        }
    }

    int get_page_fault_num() {
        return this -> page_fault_num;
    }

    void removeNode(LinkedList* node) {
        node -> prev -> next = node -> next;
        node -> next -> prev = node -> prev;
    }

    void addNodeToHead(LinkedList* node) {
        node -> prev = head;
        node -> next = head -> next;
        head -> next -> prev = node;
        head -> next = node;
    }

    void moveNodeToHead(LinkedList* node) {
        removeNode(node);
        addNodeToHead(node);
    }
    
    LinkedList* removeTailNode() {
        LinkedList* node = tail -> prev;
        removeNode(node);
        return node;
    }
};

int main(int argc, char *argv[]) {
    srand(time(NULL));
    int number = atoi(argv[1]);
    int k = atoi(argv[2]);

    vector<int> page_trace_number_serie;
    for (int i = 0; i < number; i++)
        page_trace_number_serie.push_back(rand() % k);

    vector<int> page_fault_stat;
    for (int LRU_size = 4; LRU_size <= k; LRU_size++) {
        LRUCache * testLRU = new LRUCache(LRU_size);

        for (int i = 0; i < number; i++)
            testLRU -> put(page_trace_number_serie[i]);
        
        page_fault_stat.push_back(testLRU->get_page_fault_num());
        delete testLRU;
    }

    cout << "page faults stats are: " << endl;
    for (const auto& page_fault_num: page_fault_stat)
        cout << page_fault_num << " " << endl;
    

    ofstream output_file;
    output_file.open("lab8_result.txt");

    for (const auto& page_fault_num: page_fault_stat)
        output_file << page_fault_num << endl;
    
    output_file.close();
    return 0;
}