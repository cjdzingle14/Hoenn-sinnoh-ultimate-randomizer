# Upstream Engine

Selected engine source: [LiderMorti00/Sinnoh-pokeemerald-expansion](https://github.com/LiderMorti00/Sinnoh-pokeemerald-expansion)

- Parent engine: RHH pokeemerald-expansion
- Integration: pinned Git submodule at vendor/pokeemerald-expansion
- Upstream branch used to select the pin: master
- Pinned commit: `dd06b332cc5170920dc0be923337dafb7080f327`
- Pin selected: 2026-11-16

This is a fork of RHH's pokeemerald-expansion with a large Sinnoh implementation. The selected tree contains Sinnoh map, layout, and event-script data alongside the Emerald base. Pinning an exact commit keeps builds reproducible.

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

## Integration status

The fork is now selected as the engine source so its Sinnoh data can be evaluated against our current Hoenn/randomizer changes. This pin is a source-selection milestone, not proof that both regions or the New Game choice work in a compiled ROM. Next steps are to audit the fork's map groups, map connections, events, graphics dependencies, and engine changes; reconcile them with our randomizer features; then build and test in an emulator.

Do not copy commercial ROM data or proprietary Nintendo DS assets into this repository.
