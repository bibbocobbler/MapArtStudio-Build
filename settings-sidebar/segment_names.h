#pragma once
#include <filesystem>
#include <stdexcept>
#include <string>
namespace mapart {
inline std::string segmentFileName(const std::string &folder, int topRow, int column,
                                  int rows, const char *suffix = ".nbt") {
    if (rows <= 0 || topRow < 0 || topRow >= rows || column < 0)
        throw std::invalid_argument("Invalid segment position");
    auto path = std::filesystem::path(folder).lexically_normal();
    while (path.filename().empty() && path.parent_path() != path) path = path.parent_path();
    auto prefix = path.filename().string();
    if (prefix.empty()) prefix = "mapart";
    return prefix + " " + std::to_string(rows - 1 - topRow) + "," + std::to_string(column) + suffix;
}
inline std::string legacySegmentFileName(const std::string &folder, long ordinal,
                                        int columns, int rows) {
    if (columns <= 0 || rows <= 0 || ordinal < 1 || ordinal > columns * rows)
        throw std::invalid_argument("Invalid legacy segment number");
    const int index = static_cast<int>(ordinal - 1);
    return segmentFileName(folder, index / columns, index % columns, rows);
}
}
