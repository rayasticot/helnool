#include <stdio.h>
#include <stdlib.h>
#include "map.h"

const unsigned char INTRO[3] = {width, height, 1};

void main(){
    FILE* f = fopen("exportmap.legba", "wb");
    fwrite(INTRO, 1, 3, f);
    fwrite(header_data, 1, width*height, f);
    fclose(f);
}