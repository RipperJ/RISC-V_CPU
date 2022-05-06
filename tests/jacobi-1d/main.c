#include <stdio.h>
int main() {
    int A[10], B[10];
    for (int i = 0; i < 10; i++) {
        A[i] = i + 2;
        B[i] = i + 3;
    }
    for (int t = 0; t < 5; t++) {
        for (int i = 1; i < 9; i++) {
            B[i] = A[i-1]+A[i]+A[i+1];
        }
        for (int i = 1; i < 9; i++) {
            A[i] = B[i-1]+B[i]+B[i+1];
        }
        printf("t = %d\n", t);
        for (int i = 0; i < 10; i++) {
            printf("A[%d] = %d, B[%d] = %d\n", i, A[i], i, B[i]);
        }
    }
    for (int i = 0; i < 10; i++) {
        printf("A[%d] = %d, B[%d] = %d\n", i, A[i], i, B[i]);
    }
}
