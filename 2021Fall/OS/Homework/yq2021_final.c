#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>
#include <time.h>

// function prototypes
void *thread_func(void *param);
int barrier_point();
int barrier_init();
// number of threads - obtained from an input argument

int n;
// Variables uses by the barrier
int count;
pthread_mutex_t count_lock;
sem_t semaphore, semaphore_2;

int main(int argc, char *argv[])
{
    srand(time(NULL));
    if (argc != 2) {
        printf("Error - Usage: ./final <number of threads>\n");
        return -1;
    }
    int i;
    n = atoi(argv[1]);
    pthread_t thread_ids[n];
    int thread_num[n];
    // Initialize the barrier
    if (barrier_init() != 0){
        printf("Error: barrier_init() failed\n");
        return -1;
    }
    // create the threads
    for (i = 0; i < n; i++) {
        thread_num[i] = i;
        pthread_create(&thread_ids[i], 0, thread_func, &thread_num[i]);
    }
    // wait for the threads to finish
    for (i = 0; i < n; i++)
        pthread_join(thread_ids[i], 0);
        
    return 0;
}

// The thread function
void *thread_func(void *param)
{
    int seconds;
    int thread_number = *((int*) param);
    /* Sleep for a random period of time */
    seconds = (int) ( (rand() % 5) + 1);
    printf("Thread %d going to sleep for %d seconds\n", thread_number, seconds);
    sleep(seconds);
    /* Wait at the barrier point */
    printf("Thread %d is into the barrier\n", thread_number);
    barrier_point();
    /* Now we're out of the barrier point */
    printf("Thread %d is out of the barrier\n", thread_number);
    return NULL;
}


int barrier_init()
{
    // Initialize here
    count = 0;
    if (pthread_mutex_init(&count_lock, NULL) != 0) {
        printf("mutex initialization failed!\n");
        return -1;
    }
    if (sem_init(&semaphore, 0, 1) != 0) {
        printf("semaphore initialization failed!\n");
        return -1;
    }
    if (sem_init(&semaphore_2, 0, 1) != 0) {
        printf("semaphore initialization failed!\n");
        return -1;
    }
    return 0;
}

/* The barrier point function */
int barrier_point()
{
 // put your code here
    pthread_mutex_lock(&count_lock);
    sem_wait(&semaphore);
    if(count == n - 1){
        count = 0;
        sem_post(&semaphore);
        for(int i = 0; i < n - 1; i++)
            sem_post(&semaphore_2);
    }
    else {
        count++;
        sem_post(&semaphore);
        sem_wait(&semaphore_2);
    }
    pthread_mutex_unlock(&count_lock);
    return 0;
}


// int barrier_init(barrier_t *barrier, unsigned int num_threads) {
//     int error = 0;
//     pthread_mutex_init(&(barrier->mtx), NULL);
//     pthread_cond_init(&(barrier->cv), NULL);
//     barrier->n_threads = num_threads;
//     barrier->count = 0;
//     barrier->times_used = 0;
//     return error;
// }

// int barrier_wait(barrier_t *barrier) {
//     pthread_mutex_lock(&(barrier->mtx));

//     while(barrier->count > barrier->n_threads) 
//       pthread_cond_wait(&(barrier->cv), &(barrier->mtx));
    
// //    pthread_mutex_lock(&(barrier->mtx));
//     barrier->count = barrier->count - 1;
//     if (barrier->count == 0) {
//         barrier->count = barrier->n_threads * 2 - 1; 
//         barrier->times_used++;
//     }
//     else {
//       while(barrier -> count < barrier -> n_threads) {
//         printf("count is %d.\n",barrier -> count);
//         pthread_cond_wait(&(barrier->cv), &(barrier->mtx));
//       }
//       barrier->count = barrier->count - 1;
//     }
//     pthread_cond_broadcast(&(barrier->cv));
//     pthread_mutex_unlock(&(barrier->mtx));

//     return 0;
// }