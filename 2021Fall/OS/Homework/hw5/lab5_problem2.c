#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdbool.h>
#include <semaphore.h>

pthread_t tid[5];

const int eachThreadPointsNum = 1e6;
int count = 0;

//Return if a < b
const double eps = 1e-6;
bool isLess(double a, double b) {
    return (a - b) < eps;
}

// pthread_mutex_t mutex_lock;
sem_t semaphore_mutex;

void * threadFunc() {
    for (int i = 0; i < 1000000; i++) {
        sem_wait(&semaphore_mutex);
        double xcoordinate = ((double) rand() / (double) RAND_MAX) * 2.0 - 1;
        double ycoordinate = ((double) rand() / (double) RAND_MAX) * 2.0 - 1;

        if (isless(pow(xcoordinate, 2) + pow(ycoordinate, 2), 1.0))
            count++;
        sem_post(&semaphore_mutex);
    }
}

int main() {
    srand(time(NULL));
    sem_init(&semaphore_mutex, 0, 1);

    int status;
    for (int i = 0; i < 4; i++)
        status = pthread_create(&tid[i], NULL, threadFunc, NULL);
    
    for (int i = 0; i < 4; i++)
        pthread_join(tid[i], NULL);

    sem_destroy(&semaphore_mutex);
    printf("Count is %d\n", count);
    int totalPoints = eachThreadPointsNum * 4;
    double insideRation = 4.0 * ((double) count / (double) totalPoints);
    printf("The estimated area is: %.6lf\n", insideRation);
    return 0;
}