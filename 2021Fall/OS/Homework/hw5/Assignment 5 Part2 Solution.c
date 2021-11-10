#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h> 

#define NUM_THREADS 4
#define POINTS_PER_THREAD 1000000

int incircle = 0;
pthread_mutex_t lock; 

void *runner() {
    /* Adding to a rand number to get a local random number for each thread */
    unsigned int rand_state = (unsigned int) time(NULL) + pthread_self();

    for (int i = 0; i < POINTS_PER_THREAD; i++) {
    	/* Use rand_r instead of rand since rand is not thread safe */
        double x = rand_r(&rand_state) / ((double)RAND_MAX + 1) * 2.0 - 1.0;
        double y = rand_r(&rand_state) / ((double)RAND_MAX + 1) * 2.0 - 1.0;

        if ( ((x * x) + (y * y)) < 1) {
        	pthread_mutex_lock(&lock); 
            ++incircle;
            pthread_mutex_unlock(&lock);
        }
    } 
}


int main(int argc, const char *argv[])
{
    /* Seed for the pseudo-random number */
    srand((unsigned)time(NULL));

    /* Array of threads */
    pthread_t *threads = malloc(NUM_THREADS * sizeof(pthread_t));

    pthread_attr_t attr;
    pthread_attr_init(&attr);

  	//Inititalize the lock. This can also be done using macros
    if (pthread_mutex_init(&lock, NULL) != 0) { 
        printf("Mutex init has failed\n"); 
        return -1; 
    }

    /* Create the threads */
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_create(&threads[i], &attr, runner, (void *) NULL);
    }

    /* Wait for threads to exit */
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&lock); 
    free(threads);

    printf("Pi: %f\n", (4.0 * (double)incircle) / ((double)POINTS_PER_THREAD * NUM_THREADS));

    return 0;
}
