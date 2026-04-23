from green_db import init_db, seed_hardware, save_audit_result, get_audit_history

DB = "carboncut.db"

# 1) Init + seed
init_db(DB)
seed_hardware(DB)

# 2) Insert sample audit
audit_id = save_audit_result(
    db_path=DB,
    original_code="print('hello')",
    green_code="print('hello')  # optimized",
    device_name="NVIDIA RTX 4050 (85W)",
    max_wattage=85.0,
    is_laptop=False,
    epochs_detected=5,
    grid_intensity=180.0,
    std_total_kg=0.8,
    green_total_kg=0.3,
    kg_saved=0.5,
    tree_days=0.6,
    phone_charges=0.02,
)

print("Inserted audit_id:", audit_id)

# 3) Fetch history and basic assertions
rows = get_audit_history(DB, limit=10)
assert len(rows) >= 1, "No audit rows found"
first = rows[0]
assert first["device_name"] is not None, "Missing device_name"
assert first["std_total_kg"] is not None, "Missing emission data"

print("Latest audit:", first)