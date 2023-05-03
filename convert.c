#include <stdio.h>
#include <stdlib.h>
#include "img.h"

const unsigned char INTRO[3] = {width, height, 0};

void main(){
    FILE* f = fopen("export.legba", "wb");
    fwrite(INTRO, 1, 3, f);
    for(int i = 0; i < width*height; i++){
        header_data[i] += 17;
    }
    fwrite(header_data, 1, width*height, f);
    fclose(f);
}