#include <linux/miscdevice.h>
#include <linux/module.h>
#include <linux/init.h>
#include <linux/fs.h>
#include <linux/time.h>
#include <linux/jiffies.h>
#include <asm/param.h>

static char time_since_last_booted[100]; //record the required info 

static int my_miscDevice_open(struct inode* pinode, struct file* pfile) {
    int tick_time = 1000 / HZ; // compute tick time 
    //Get the time period since the system was booted.
    //It should be noticed that "jiffies" are initialized with the macro "INITIAL_JIFFIES", not the "0" when system was booted
    unsigned long current_time = (get_jiffies_64() - INITIAL_JIFFIES) * tick_time;
    
    unsigned long seconds, milliseconds;
    //convert to seconds and milliseconds.
    seconds = current_time / 1000;
    milliseconds = current_time % 1000;
    printk(KERN_WARNING "myDevice is opened!\n");
    sprintf(time_since_last_booted, "Hello world, the time since boot %lu.%lu seconds.\n ", seconds, milliseconds);
    return 0;
}

static int my_miscDevice_release(struct inode* pinode, struct file* pfile) {
    printk("my_miscDevice is released!\n");
    return 0;
}

static ssize_t my_miscDevice_read(struct file* pfile, char* content, size_t length, loff_t* offset) {
    size_t len = strlen(time_since_last_booted);

    // If the offset position is equal to the length, then stop reading the device file. 
    // If we do not update the offset value and do this judgement, then the read function will keep printing the information.
	if (*offset == len)
		return 0;

    //Copy content to user_space
    unsigned long result = copy_to_user(content, time_since_last_booted, strlen(time_since_last_booted));

    //Judge if copy_to_user is successful or not
    if (result == 0) 
        printk(KERN_WARNING "copy_to_user successful!\n");
    else {
        printk(KERN_WARNING "copy_to_user failed!\n");
        return -1;
    }

    //Update the offset. 
	*offset += len;
	return len;
}


static const struct file_operations my_miscDevice_fops = {
    .open = my_miscDevice_open,
    .release = my_miscDevice_release,
    .read = my_miscDevice_read
};

static struct miscdevice my_miscDevice = {
    .fops = &my_miscDevice_fops,
    .name = "lab3_problem2",
    .minor = MISC_DYNAMIC_MINOR,
};

static int __init  hello_init(void) {
    int result = misc_register(&my_miscDevice);
    if (result < 0) {
        printk(KERN_ALERT "Register my Misc_Device failed!\n");
        return -1;
    }
    
    printk(KERN_INFO "Register my Misc_Deivce successful!\n");
    return 0;
}

static void __exit hello_exit(void) {
    misc_deregister(&my_miscDevice);
    printk(KERN_INFO "My Misc_Deivce has been deregistered!\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Yinhong Qin");
MODULE_DESCRIPTION("The contents of CS 6223 homework 3, problem2.");


//This code is finished by Yinhong Qin, with netID yq2021 and student ID N14457656.