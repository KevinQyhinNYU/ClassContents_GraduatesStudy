#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <sys/wait.h>



int main(int argc,char *argv[]){
	if (argc != 3) {
		printf("Please input two parameters: n and d.\n");
		return 0;
	}
	
	int n,d;
	n = atoi(argv[1]);
	d = atoi(argv[2]);
	
	// create the ordinary pipes
    int fd[2];
    
    if (pipe(fd) == -1){
        perror("Pipe failed!");
    }

	pid_t pid = fork();
	if (pid < 0) {
		printf("Fork failed!");
		return -1;
	} else if (pid == 0){
		int c = 0, interval, val;
		
		// disable reading
		close(fd[0]);
		
		// set the seed
		srand((unsigned) time(NULL));
		
		while(c < n){
			val = d * c;
			
			// write to the pipe
			write(fd[1], &val, sizeof(int));

			// wait for a random interval of time (0 to 9.999 seconds)
			interval = rand() % 10000;
			usleep(interval * 1000);
			
			c++;
		}
		
		// disable writing
		close(fd[1]);
	} else {
		int c = 0, val;
		
		// disable writing
		close(fd[1]);
	
		while(c < n){
			c++;
			
			// read from the pipe
			read(fd[0], &val, sizeof(int));
			printf("%d ", val);
			fflush(stdout);
		}

		printf("\n");
		fflush(stdout);
		
		// disable reading
		close(fd[0]);
	}

	return 0;
}
