#include<stdio.h>
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

int number = 0;
int diff = 0;

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
    printf("In producer, the address of number is: %p\n", &number);
    printf("In producer, the address of diff is: %p\n", &diff);

    sharedMemoryBuffer *shared_memory;
    int sharedMemory_fd = shm_open("lab7", O_CREAT | O_RDWR, 0666);
    ftruncate(sharedMemory_fd, sizeof(sharedMemoryBuffer));

    shared_memory = mmap(0, sizeof(sharedMemoryBuffer), PROT_READ | PROT_WRITE, MAP_SHARED, sharedMemory_fd, 0);
    
    //Initialize the pointers used in buffer queue
    shared_memory -> sharedMemoryHead = 0;
    shared_memory -> sharedMemoryTail = 0;
    
    if (shared_memory == MAP_FAILED) {
        printf("Map Failed!\n");
        return -1;
    }
    
    printf("In producer, starting address of shared memory is: %p\n", shared_memory -> bufferQueue);

    printf("In producer program, goona produce number.\n");
    for (int i = 0; i < number; i++) {
        // if head == tail + 1, it means that the buffer is full of numbers. Then child process should wait until there are some empty space in the buffer.
        while ((shared_memory -> sharedMemoryTail + 1) % BUFFER_SIZE == shared_memory -> sharedMemoryHead); 
        int currentValue = i * diff;
        shared_memory -> bufferQueue[shared_memory -> sharedMemoryTail] = currentValue;
        shared_memory -> sharedMemoryTail = (shared_memory -> sharedMemoryTail + 1) % BUFFER_SIZE;
        
        printf("In producer program, The %dth value is: %d\n", i, currentValue);
        int waitTime = (rand() % 10000);
        printf("Going to sleep %d ms\n", waitTime);

        struct timespec ts;
        ts.tv_sec = waitTime / 1000;
        ts.tv_nsec = (waitTime % 1000) * 1e6;
        nanosleep(&ts, &ts);
        fflush(stdout);
    }
    return 0;
}