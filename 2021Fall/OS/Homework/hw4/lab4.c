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

#define BUFFER_SIZE 100

//Define the buffer queue, head index and tail index
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
    
    //Get the parameters 'n' and 'd'
    int number = atoi(argv[1]);
    int diff = atoi(argv[2]);

    sharedMemoryBuffer *shared_memory;
    int sharedMemory_fd = shm_open("hw4_lab", O_CREAT | O_RDWR, 0666);
    ftruncate(sharedMemory_fd, sizeof(sharedMemoryBuffer));

    shared_memory = mmap(0, sizeof(sharedMemoryBuffer), PROT_WRITE, MAP_SHARED, sharedMemory_fd, 0);
    
    //Initialize the pointers used in buffer queue
    shared_memory -> sharedMemoryHead = 0;
    shared_memory -> sharedMemoryTail = 0;
    
    if (shared_memory == MAP_FAILED) {
        printf("Map Failed!\n");
        return -1;
    }
    
    pid_t pid = fork();

    if (pid == -1) {
        printf("fork() Failed!");
        exit(1);
    }

    // Child process
    else if (pid == 0) {
        for (int i = 0; i < number; i++) {
            // if head == tail + 1, it means that the buffer is full of numbers. Then child process should wait until there are some empty space in the buffer.
            while ((shared_memory -> sharedMemoryTail + 1) % BUFFER_SIZE == shared_memory -> sharedMemoryHead); 
            int currentValue = i * diff;
            shared_memory -> bufferQueue[shared_memory -> sharedMemoryTail] = currentValue;
            shared_memory -> sharedMemoryTail = (shared_memory -> sharedMemoryTail + 1) % BUFFER_SIZE;
            
            printf("In child process, The %dth value is: %d\n", i, currentValue);
            int waitTime = (rand() % 10000);
            printf("Going to sleep %d ms\n", waitTime);

            struct timespec ts;
            ts.tv_sec = waitTime / 1000;
            ts.tv_nsec = (waitTime % 1000) * 1e6;
            nanosleep(&ts, &ts);
        fflush(stdout);
        }
        exit(0);
    }
    
    // Parent process
    else if (pid > 0) {
        for (int i = 0; i < number; i++) {
            //if head == tail + 1, it means that the buffer is empty. Then it need to wait the buffer become non-empty.
            while (shared_memory -> sharedMemoryHead == shared_memory -> sharedMemoryTail);
            printf("In parent process, Read value at the %dth position is: %d\n", i, shared_memory -> bufferQueue[shared_memory -> sharedMemoryHead]);
            shared_memory -> sharedMemoryHead = (shared_memory -> sharedMemoryHead + 1) % BUFFER_SIZE;
            fflush(stdout);  
        }
        exit(0);
    }

    shm_unlink("hw4_lab");
    return 0;
}


//This code is finished by Yinhong Qin, with netID yq2021.