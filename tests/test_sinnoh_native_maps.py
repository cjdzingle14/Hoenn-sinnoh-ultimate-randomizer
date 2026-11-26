import json
import tempfile
import unittest
from pathlib import Path

from tools.validate_sinnoh_engine_maps import validate


class NativeSinnohMapTests(unittest.TestCase):
    def test_manifest_uses_real_engine_maps_and_connected_start_slice(self):
        root = Path(__file__).resolve().parents[1]
        engine = root / "vendor/pokeemerald-expansion"
        if not engine.exists():
            self.skipTest("pinned engine submodule is not checked out")
        errors = validate(engine, root / "config/sinnoh_world_slice.json")
        self.assertEqual(errors, [])

    def test_rejects_a_manifest_map_id_that_does_not_match_engine(self):
        root = Path(__file__).resolve().parents[1]
        engine = root / "vendor/pokeemerald-expansion"
        if not engine.exists():
            self.skipTest("pinned engine submodule is not checked out")
        manifest = json.loads((root / "config/sinnoh_world_slice.json").read_text())
        manifest["maps"][0]["id"] = "MAP_NOT_A_REAL_TWINLEAF_MAP"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manifest.json"
            path.write_text(json.dumps(manifest))
            errors = validate(engine, path)
        self.assertTrue(any("does not match native id" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
