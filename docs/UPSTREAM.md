# Upstream Engine

Selected upstream: [RHH pokeemerald-expansion](https://github.com/rh-hideout/pokeemerald-expansion)

- Repository: https://github.com/rh-hideout/pokeemerald-expansion
- Integration: Git submodule at vendor/pokeemerald-expansion
- Upstream branch used to select the pin: master
- Pinned commit: `4da9230cf7c1f1d7b0d47b45783b202666fffece`
- Pin selected: 2026-11-13
- Baseline build: initial Ubuntu 22.04 / GCC 10 attempt reached compilation but failed on C label/declaration compatibility in upstream source; CI is being retried on Ubuntu 24.04 with a newer ARM GCC toolchain.

The source is pinned to an exact upstream commit so builds do not silently change when the upstream branch moves. The submodule points to the upstream project directly and preserves its own Git history.

## Checkout

Clone this repository with submodules enabled:

```bash
git clone --recurse-submodules https://github.com/cjdzingle14/Hoenn-sinnoh-ultimate-randomizer.git
cd Hoenn-sinnoh-ultimate-randomizer
git submodule status
```

If the project was already cloned without submodules:

```bash
git submodule update --init --recursive
```

## Baseline build gate

Before making engine-specific changes:

1. Follow the upstream [installation and build instructions](https://github.com/rh-hideout/pokeemerald-expansion/blob/4da9230cf7c1f1d7b0d47b45783b202666fffece/INSTALL.md).
2. Build the unmodified upstream checkout.
3. Record the operating system, toolchain versions, build command, and result here.
4. Only after a clean baseline build, begin importing Sinnoh maps and adding game-specific engine code.

The upstream project is a decompilation-based GBA ROM-hack development base, not a playable game by itself. Do not add commercial Pokémon ROMs or proprietary assets to this repository.
