#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/shm.h>
#include <sys/stat.h>
#include<unistd.h>
#include<sys/types.h>
#include<string.h>
#include<sys/wait.h>
#include<time.h>
#include<sys/mman.h>
#include <sys/ipc.h>

#define BUF_SZ 10

typedef struct {
	int in;
	int out;
	int buffer[BUF_SZ];
} block;

int nn = 0, dd = 0;

int main(int argc,char *argv[]){

	if (argc != 3) {
		printf("Please input two parameters: n and d.\n");
		return 0;
	}
	
	nn = atoi(argv[1]);
	dd = atoi(argv[2]);
	
	printf("Address of n: %p\n", &nn);
	
	// create shared memory object
    int shm_fd = shm_open("/lab7", O_CREAT | O_RDWR, 0666);
	
	ftruncate(shm_fd, sizeof(block));
	
	// create the shared buffer
	void* ptr = mmap(0, sizeof(block), PROT_WRITE, MAP_SHARED, shm_fd, 0);
	
	printf("Start address of the shared buffer: %p\n", ptr);
	
	int c = 0;
	block* shared_block = ptr;
	
	while(c < nn){
		// wait till buffer is not empty
		while(shared_block->in == shared_block->out);
		
		c++;

		printf("%d ", shared_block->buffer[shared_block->out]);
		fflush(stdout);

		shared_block->out = (shared_block->out+ 1) % BUF_SZ;
	}

	printf("\n");
	fflush(stdout);

	// remove the shared buffer
	munmap(ptr, sizeof(block));
	return 0;

}
