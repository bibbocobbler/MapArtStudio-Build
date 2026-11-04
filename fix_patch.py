from pathlib import Path
p = Path("apply_upgrade.py")
s = p.read_text(encoding="utf-8")
old = "'    double d2;\\n    // Compute data'"
new = "'    double d2;\\n\\n    // Compute data'"
if old not in s:
    raise SystemExit("Expected original map_generate anchor not found")
p.write_text(s.replace(old,new,1),encoding="utf-8")
print("Adjusted patch for upstream map_generate.cpp whitespace")
