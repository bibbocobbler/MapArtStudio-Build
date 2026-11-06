# ImageToMapMC — Original UI + Colour Approximation Options

This repository builds an enhanced Windows x64 version of [AgustinSRG/ImageToMapMC](https://github.com/AgustinSRG/ImageToMapMC), retaining its **original wxWidgets interface**.

The existing **Color approximation** menu has six choices:

| Menu choice | Description |
| --- | --- |
| Euclidean RGB | Original squared RGB distance |
| Delta E (CIE76) | Original CIELAB distance |
| OKLab | Perceptual OKLab distance; default for new projects |
| CIEDE2000 | Advanced perceptual CIEDE2000 colour difference |
| Weighted RGB (Redmean) | Channel-weighted RGB with redmean adjustment |
| Linear RGB | Linear-light RGB with luminance weighting |

The chosen method is used for preview generation and map/structure export, and is saved and loaded with the project. The console program supports `--color-method euclidean|delta-e|oklab|ciede2000|redmean|linear-rgb`.

**Preserved:** original two-panel window, menus and native colours, Minecraft 26.2 version option, remembered material presets, high-quality resizing, Floyd–Steinberg accuracy fix, existing map/structure/schematic export paths.

## Windows EXE

Open [Actions → Build Original UI - Six Colour Methods](https://github.com/bibbocobbler/MapArtStudio-Build/actions/workflows/build-original-ui.yml). Choose the latest **successful** run, scroll to **Artifacts**, and download `MapArtStudio-OriginalUI-Windows-x64`. Extract the ZIP and run `mcmap-gui.exe`, keeping its DLL files alongside it.

The build compiles C++ sources using Visual Studio and vcpkg on a Windows GitHub runner. It does **not** run Minecraft to validate exported NBTs. Test exports in a backup world before relying on them.

The GitHub upstream code is not the same as any separately modified V6 binary. Features unique to the V6 binary may not be present in this build.

## Development

The workflow downloads upstream ImageToMapMC, applies the prior engine fixes and then applies `original-ui/patch.b64` (a SHA-256 verified compressed archive containing `enhance_original_ui.py`, `color_metrics.h`, and the CIEDE2000 metric tests). The original UI source files are restored from the upstream Git revision before colour menu additions.

CIEDE2000 was checked against published reference colour-pair values. It may be slower than Euclidean/Redmean on large images.

This project follows the upstream ImageToMapMC license.
