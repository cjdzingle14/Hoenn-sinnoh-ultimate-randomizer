"""Make trade-based evolutions available through normal level-up checks."""
from __future__ import annotations

import argparse
from pathlib import Path


def patch_trade_evolutions(source: str) -> str:
    """Treat EVO_TRADE as a level-up trigger; keep held-item conditions intact."""
    old = """            case EVO_LEVEL_BATTLE_ONLY:
                if (mode == EVO_MODE_BATTLE_ONLY && evolutions[i].param <= level)
                    conditionsMet = TRUE;
                break;
"""
    new = old + """            case EVO_TRADE:
                // Trade evolutions are available on the next level-up at level 37 or higher.
                if (level >= 37)
                    conditionsMet = TRUE;
                break;
"""
    if new not in source:
        if source.count(old) != 1:
            raise ValueError("Could not uniquely locate normal evolution method switch")
        source = source.replace(old, new, 1)

    old_condition = """        case IF_TRADE_PARTNER_SPECIES:
            if (params[i].arg1 == partnerSpecies && partnerHoldEffect != HOLD_EFFECT_PREVENT_EVOLVE)
                currentCondition = TRUE;
            break;
"""
    new_condition = """        case IF_TRADE_PARTNER_SPECIES:
            // Without link trading, partner-specific trade evolutions are also level-up evolutions.
            if (tradePartner == NULL
                || (params[i].arg1 == partnerSpecies && partnerHoldEffect != HOLD_EFFECT_PREVENT_EVOLVE))
                currentCondition = TRUE;
            break;
"""
    if new_condition not in source:
        if source.count(old_condition) != 1:
            raise ValueError("Could not uniquely locate trade-partner evolution condition")
        source = source.replace(old_condition, new_condition, 1)
    return source


def integrate(engine_dir: Path) -> None:
    path = engine_dir / "src" / "pokemon.c"
    source = path.read_text(encoding="utf-8")
    path.write_text(patch_trade_evolutions(source), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine-dir", type=Path, required=True)
    args = parser.parse_args()
    integrate(args.engine_dir)
    print("Integrated trade-free level-up evolutions")


if __name__ == "__main__":
    main()
