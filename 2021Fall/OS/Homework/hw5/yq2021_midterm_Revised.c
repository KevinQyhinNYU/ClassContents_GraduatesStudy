#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>

const int pointsNum = 1e6;

int main() {
    srand(time(NULL));
    int pipeline[4][2]; // 1 - write.  0 - read
    
    pid_t pid;
    int i;
    for (i = 0; i < 4; i++) {
        if (pipe(pipeline[i]) < 0) {
            printf("Creating pipeline failed!\n");
            exit(1);
        }
        
        pid = fork();

        if (pid == 0 || pid < 0) 
            break;
    }

    if (pid < 0) {
        printf("Create child process failed!\n");
        exit(1);
    }

    if (pid == 0) {
        //In child process;
        //First we close the read end of the pipe
        printf("In child process, gonna close the %dth pipe read end.\n", i);

        int counter = 0;
        close(pipeline[i][0]);

        unsigned int randState = (unsigned int)(time(NULL)) + (unsigned int)(getpid());
        //Generate points and doing statistics
        for (int i = 0; i < pointsNum; i++) {
            double xCoordinate = ((double)rand_r(&randState) / (double)(RAND_MAX + 1.0)) * 2.0 - 1.0;
            double yCoordinate = ((double)rand_r(&randState) / (double)(RAND_MAX + 1.0)) * 2.0 - 1.0;

            if (xCoordinate * xCoordinate + yCoordinate * yCoordinate < 1.0)
                counter++;
        }
        //Write the value of count to the pipe.
        write(pipeline[i][1], &counter, sizeof(int));
        
        //Finally close the write end of the pipe in child process and exit.
        close(pipeline[i][1]);
        exit(0);
    }
    else {
        //In parent process;
        //First we close the write end of the pipe in parent process.
        for (int j = 0; j < 4; j++)
            close(pipeline[j][1]);

        wait(NULL);

        int totalCount = 0;
        for (int j = 0; j < 4; j++) {
            int val;
            //Read value from the pipe
            read(pipeline[j][0], &val, sizeof(int));
            printf("In parent process, from the %dth pipe, read data is %d.\n", j, val);
            totalCount += val;
        }

        for (int j = 0; j < 4; j++)
            close(pipeline[j][0]);

        double ans = 4.0 * ((double)totalCount / (double)(4 * pointsNum));
        //Output the answer
        printf("The estimated value of pi is: %.6lf \n", ans);
    }
    return 0;
}