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

## Screenshot-style right-hand settings panel (current build)

The [Build Sidebar - Six Colour Methods](https://github.com/bibbocobbler/MapArtStudio-Build/actions/workflows/build-sidebar.yml) Windows workflow reconstructs the right-hand settings panel shown in the user's V6 reference screenshot. It contains live image size controls, image edit access, Minecraft version, dithering, all six colour approximation choices, build method selection, support settings, material choice, and export buttons.

**Important distinction:** The C++ source checked out from AgustinSRG does not include the V6-specific stacked-carpet generator, carpets-on-string exporter, or the V6 build-method comparison dialog. To avoid silently writing ordinary staircases as carpet NBT, the new GUI delegates carpet exports to the **original V6 CLI binary** supplied with the original ZIP.

Extract the artifact and then put the user's supplied V6 `mcmap.exe` next to the new `mcmap-gui.exe` **renamed to `mcmap-legacy.exe`**. Choose 3D Stacked Carpets or 3D Carpets on String in the new sidebar and export; the new six-method preview is supplied as a pre-colour-matched PNG to the V6 converter. The original V6 CLI handles carpet geometry and 128×129 segmented structures. The original V6 application is a required companion only for these carpet modes.

- Standard Flat / Staircased / 3D Complex exports use the freshly compiled C++ engine.
- The Build Method comparison dialog is not ported to the new UI; use the separately preserved original V6 GUI for that feature.
- The original V6 CLI targets 26.1 structure format; **Minecraft 26.2 compatibility must be tested** before automated printing. Limiting stacked carpets to 2–5 layers may alter the visible shades; preview matching is not an in-game rendering guarantee.
- Only compile and workflow-level checks are automated; there is no Windows GUI interaction or in-game NBT test.
