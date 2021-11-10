#include<stdio.h>
#include<stdlib.h>
#include<time.h>
#include<fcntl.h>
#include<string.h>
#include<errno.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<unistd.h>
#include<arpa/inet.h>

int main(int argc, char *argv[]) {
    srand(time(NULL));
    if (argv[1] < 0) {
        printf("The number entered is not valid!\n");
        exit(1);
    }
    
    //Get the parameters 'n' and 'd'
    int number = atoi(argv[1]);
    int diff = atoi(argv[2]);

    pid_t childPid;

    if ((childPid = fork()) < 0) {
        printf("Create child process failed!\n");
        exit(1);
    }
    
    if (childPid == 0) {
        //In child process, create the server socket and producer
        int serverSocket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        if (serverSocket < 0) {
            printf("Server socket creation failed!\n");
            exit(1);
        }

        struct sockaddr_in serverSocketAddress;
        socklen_t serverSocketAddressLength = sizeof(serverSocketAddress);
        memset(&serverSocketAddress, 0, serverSocketAddressLength);

        //Set address parameters
        serverSocketAddress.sin_family = AF_INET;
        serverSocketAddress.sin_addr.s_addr = inet_addr("127.0.0.1");
        serverSocketAddress.sin_port = htons(9527);

        int ret;
        ret = bind(serverSocket, (struct sockaddr*)&serverSocketAddress, serverSocketAddressLength);
        if (ret < 0) {
            printf("Server Socket binding failed!\n");
            exit(1);
        }
        
        //Waiting for a random time
        int waitingTime = rand() % 4001 + 1000;
        printf("In child process, goiong to sleep for %d ms.\n", waitingTime);

        struct timespec ts;
        ts.tv_sec = waitingTime / 1000;
        ts.tv_nsec = (waitingTime % 1000) * 1e6;
        nanosleep(&ts, &ts);

        ret = listen(serverSocket, 20);
        if (ret < 0) {
            printf("Server Socket listening failed!\n");
            exit(1);
        }

        //Accept for clients. Blocked until connected with a client
        struct sockaddr_in clientSocketAddress;
        socklen_t clientSocketAddressLength = sizeof(clientSocketAddress);
        int clientSocket = accept(serverSocket, (struct sockaddr*)&clientSocketAddress, &clientSocketAddressLength);

        for (int i = 0; i < number; i++) {
            int generatedVal = i * diff;

            write(clientSocket, &generatedVal, sizeof(int));
            waitingTime = rand() % 10000;
            printf("In child process, write number: %d to socket and waiting for %d ms.\n", generatedVal, waitingTime);
            ts.tv_sec = waitingTime / 1000;
            ts.tv_nsec = (waitingTime % 1000) * 1e6;
            nanosleep(&ts, &ts);

        }
        
        close(serverSocket);
        close(clientSocket);
    }
    else {
        //In parent process, create the client socket and consumer
        int clientSocket = socket(AF_INET, SOCK_STREAM, 0);
        if (clientSocket < 0) {
            printf("Client Socket create failed.\n");
            exit(1);
        }

        struct sockaddr_in serverAddress;
        socklen_t serverAddressLength = sizeof(serverAddress);
        memset(&serverAddress, 0, serverAddressLength);

        serverAddress.sin_family = AF_INET;
        serverAddress.sin_addr.s_addr = inet_addr("127.0.0.1");
        serverAddress.sin_port = htons(9527);

        int ret;
        //Try to connect to the server
        printf("In parent process, try to connect to the server in Child Process.\n");
        while (1) {
            ret = connect(clientSocket, (struct sockaddr*)&serverAddress, serverAddressLength);
            if (ret == 0) {
                printf("Successfully connected to the server!\n");
                break;
            }
            else {
                printf("Connect to the server failed, going to wait for 100ms and retry. The error value is: %d.\n", errno);

                struct timespec ts;
                ts.tv_sec = 0;
                ts.tv_nsec = 1e8;
                nanosleep(&ts, &ts);
            }
        }

        //Starting read numbers
        int readVal;
        for (int i = 0; i < number; i++) {
            read(clientSocket, &readVal, sizeof(readVal));
            printf("In parent process, value read from socket is: %d\n", readVal);
        }

        close(clientSocket);
    }
    return 0;
}