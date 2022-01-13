#include <math.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#define ISPOW2(x) ((x) > 0 && !((x) & (x-1)))

int main(int argc, char **argv){
    int num = 145689;
    printf("Is %d a perfect power of 2? %d\n", num, ISPOW2(num));
    printf("%f is the log of %d\n", log(num), num);
    printf("%f is the next power of 2 of %d\n", pow(2,floor((log(num)/log(2)) + 1)), num);
    printf("%f is 2^17, %f is 2^11\n", pow(2, 17), pow(2,11));
}
