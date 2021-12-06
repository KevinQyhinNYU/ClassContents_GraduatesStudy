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

int nn = 10, dd = 10;

int main(int argc,char *argv[]){

	if (argc != 3) {
		printf("Please input two parameters: n and d.\n");
		return 0;
	}
	
	nn = atoi(argv[1]);
	dd = atoi(argv[2]);
	
	printf("Address of n: %p\n", &nn);
	
	// create shared memory object
    int shm_fd = shm_open("/lab7", O_RDWR, 0666);
	
	// create the shared buffer
	void* ptr = mmap(0, sizeof(block), PROT_WRITE, MAP_SHARED, shm_fd, 0);
	
	printf("Start address of the shared buffer: %p\n", ptr);
	
	int c = 0, interval;
	block* shared_block = ptr;
	
	// set the seed
	srand((unsigned) time(NULL));
	
	while(c < nn){
		// wait till buffer is not full
		while((shared_block->in + 1) % BUF_SZ == shared_block->out);
		
		shared_block->buffer[shared_block->in] = dd * c;
		shared_block->in = (shared_block->in + 1) % BUF_SZ;

		// wait for a random interval of time (0 to 9.999 seconds)
		interval = rand() % 10000;
		usleep(interval * 1000);
		
		c++;
	}

	// remove the shared buffer
	munmap(ptr, sizeof(block));
	return 0;

}


/* a. */
/* i. No. The shared buffer has the same phisical address, but different virtual address in both processes. */
/* ii. Virtual address. */

/* b. */
/* i. No. */
/* ii. When loading a program into the memory, sections within the executable are placed in different regions of the virtual address space of the process. 
The entire space of the process does not necessarily start at address zero. 
In addition, holes in the virutal address space may also exist to accomodate for additional memory allcoations (e.g. with malloc or mmap) */

/* 1. List two main similarities between fixed sized partitioning and paging */

/* a. Memory is divided into parts with fixed size. */
/* b. Internal memory fragmentation happens. */

/* 2. List two main similarities between variable sized partitioning and segmentation */

/* a. Memory is divided into parts with variable size. */
/* b. External memory fragmentation happens. */

/* 3. List two main differences between paging and segmentation */

/* a. Size: In paging, the size of a page is fixed whereas in segmentation, the program is divided into variable sized sections. */
/* b. Fragmentation: Paging can lead to internal fragmentation whereas segmentation risks external fragmentation. */
/* c. Logical addresses: In paging, the logical address is formed by concatenating the page number bits (most significant bits) and the page offset bits (least significant bits), 
e.g. If the logical address is formed of N bits and the pages are of size 2 k , 
then the page number will be the upper (N-K) bits of the N-bits address and the page offset will be the lower k bits of the address. 

In segmentation however, logical addresses are specified as a 2-tuple, (segment number, segment offset). */



