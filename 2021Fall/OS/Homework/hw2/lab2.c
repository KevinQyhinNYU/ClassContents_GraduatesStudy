#include<linux/init.h>
#include<linux/kernel.h>
#include<linux/module.h>
#include<asm/param.h>
#include<linux/jiffies.h>

static unsigned long time_insert_module = 0; // record the time of insertion of this module
static int tick_time = 0; // the tick time of Ubuntu 20.04.3 LTS, Linux Kernel version is 5.11.0-34.

static int __init  hello_init(void) {
    time_insert_module = get_jiffies_64();

    printk(KERN_ALERT "Hello, world!\n");
    
    tick_time = 1000 / HZ; // convert it to milliseconds
    printk(KERN_ALERT "The tick time is: %d ms\n", tick_time);

    return 0;
}

static void __exit hello_exit(void) {
    unsigned long time_diff, sec, millisec;
    
    printk(KERN_ALERT "Goodbye, curel world!\n");

    //According to the comments in <linux/jiffies.h>, it is better to read the "jiffies" variable 
    //using the function "get_jiffies_64()" since the "jiffies" is not atomic.
    
    //To calculate the time difference between removal and insertion of this module,
    //using get_jiffies_64() to get the latest value of jiffies and then minus the recorded insertion time. 
    time_diff = (get_jiffies_64() - time_insert_module) * tick_time;
    sec = time_diff / 1000;
    millisec = time_diff % 1000;
    printk(KERN_ALERT "The time between the insertion and removal of this module is: %lu s. %lu ms\n", sec, millisec);
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("Dual BSD/ GPL");
MODULE_AUTHOR("Yinhong Qin");
MODULE_DESCRIPTION("The contents of CS 6223 homework 2.");


//This code is finished by Yinhong Qin, with netID yq2021 and student ID N14457656.