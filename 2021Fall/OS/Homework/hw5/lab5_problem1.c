#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

int main(int argc, char* argv[]) {
    int seqNum = atoi(argv[1]);
    int diff = atoi(argv[2]);

    if (seqNum < 0) {
        printf("Incvalid length of sequence!\n");
        exit(1);
    }

    int pipeLine[2];
    pipe(pipeLine);
 
    pid_t childPid;

    childPid = fork();
    if (childPid < 0) {
        printf("Fork Failed!\n");
        exit(1);
    }

    if (childPid == 0) {
        //In child process, we close the read side of the pipe
        close(pipeLine[0]);
        for (int i = 0; i < seqNum; i++) {
            int seqVal = i * diff;
            char valueText[20];
            sprintf(valueText, "%d", seqVal);
            printf("In child process, the next number is: %d\n", seqVal);
            write(pipeLine[1], valueText, strlen(valueText) + 1);
        }
        //When child process is going to exit, it shuold close the write side of the pipe
        close(pipeLine[1]);
        exit(0);
    }
    else {
        //In parent process, we close the write side of the pipe
        close(pipeLine[1]);
        int readBytes;
        char readText[20];
        for (int i = 0; i < seqNum; i++) {
            while ((readBytes = read(pipeLine[0], readText, 20)) > 0)
                printf("In parent process, read value is: %s\n", readText);
        }
        //When parent process is going to exit, it shuold close the read side of the pipe
        close(pipeLine[0]);
    }

    return 0;
}