#include <stdlib.h>
int main() {
    setuid(0);
    system("cat /root/.REPLACE/flag");
    return 0;
}