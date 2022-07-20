#include <stdio.h>

int a = 100

int main(void):
  printf("hello world")
  int i = 500

  for (int j; j<i; j++):
    printf("%d", j)
    for (int t=0; t<j; t++):
      int sum = i + j+ t
      printf("sum : %d\n", sum)
      if (sum > 1024):
        printf("Over!\n\n")
      else:
        printf("Under!\n\n")
  printf("\n\n\nEnd!!\n\n\n")

  return 0
