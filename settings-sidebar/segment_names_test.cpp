#include "mapart/segment_names.h"
#include <iostream>
int main() {
    for (int top = 0; top < 2; ++top) for (int column = 0; column < 3; ++column) {
        const auto expected = "North Wall " + std::to_string(1-top) + "," + std::to_string(column) + ".nbt";
        if (mapart::segmentFileName("C:/exports/North Wall/",top,column,2) != expected ||
            mapart::legacySegmentFileName("C:/exports/North Wall",top*3+column+1,3,2) != expected) return 1;
    }
    if (mapart::segmentFileName("North Wall",0,0,1) != "North Wall 0,0.nbt") return 2;
    if (mapart::segmentFileName("North Wall",0,0,1," base.nbt") != "North Wall 0,0 base.nbt") return 3;
    for (long bad : {0L,7L}) {
        try { mapart::legacySegmentFileName("North Wall",bad,3,2); return 4; }
        catch (const std::invalid_argument &) {}
    }
    std::cout << "Native and legacy coordinate naming tests passed\n";
}
