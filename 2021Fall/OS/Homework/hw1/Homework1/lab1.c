#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    printf("Hello world! This is CS6233 Fall 2021.\n");
    
    srand(time(NULL));
    printf("%d\n\n", rand() % 100);
    return 0;
}
//This code is finished by Yinhong Qin, with netID yq2021 and student ID N14457656.