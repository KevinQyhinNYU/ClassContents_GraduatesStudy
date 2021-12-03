#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/mman.h>
#include <fcntl.h>
#include <time.h>
#include <string.h>

#define BUFFER_SIZE 50

int number = 1;
int diff = 1;

typedef struct {
    int bufferQueue[BUFFER_SIZE];

    int sharedMemoryHead;
    int sharedMemoryTail;
} sharedMemoryBuffer;

int main(int argc, char *argv[]) {
    srand(time(NULL));

    //Check if the number entered is valid (> 0)
    if (argv[1] < 0) {
        printf("The number entered is not valid!\n");
        exit(1);
    }

    number = atoi(argv[1]);
    diff = atoi(argv[2]);
    printf("In consumer, the address of number is: %p\n", &number);
    printf("In consumer, the address of diff is: %p\n", &diff);

    sharedMemoryBuffer *shared_memory;
    int sharedMemory_fd = shm_open("lab7", O_RDWR, 0666);

    shared_memory = mmap(0, sizeof(sharedMemoryBuffer), PROT_READ | PROT_WRITE, MAP_SHARED, sharedMemory_fd, 0);

    printf("shared_memory_fd is: %d\n", sharedMemory_fd);
    printf("In consumer, starting address of shared memory is: %p\n", shared_memory->bufferQueue);
    if (shared_memory == MAP_FAILED) {
        printf("Map Failed!\n");
        return -1;
    }

    for (int i = 0; i < number; i++) {
        //if head == tail + 1, it means that the buffer is empty. Then it need to wait the buffer become non-empty.
        while (shared_memory -> sharedMemoryHead == shared_memory -> sharedMemoryTail);
        printf("In consumer program, Read value at the %dth position is: %d\n", i, shared_memory -> bufferQueue[shared_memory -> sharedMemoryHead]);
        shared_memory -> sharedMemoryHead = (shared_memory -> sharedMemoryHead + 1) % BUFFER_SIZE;
        fflush(stdout);  
    }
    shm_unlink("lab7");
    return 0;
}