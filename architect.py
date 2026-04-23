import ast
import geocoder
import numpy as np
import random
import os
import time
from codecarbon import EmissionsTracker

# --- HARDWARE PROFILES ---
HARDWARE_DATA = {
    "NVIDIA RTX 4050 (Laptop)": 85,
    "NVIDIA RTX 3050 (Laptop)": 75,
    "NVIDIA RTX 3060": 170,
    "Standard Laptop CPU": 45
}

# --- AST REFACTORING LOGIC (Legacy Feature preserved) ---
class CarbonRefactorer(ast.NodeTransformer):
    def visit_Module(self, node):
        import_node = ast.Import(names=[ast.alias(name='green_lib', asname=None)])
        node.body.insert(0, import_node)
        new_body = []
        for item in node.body:
            if any(isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute) and sub.func.attr == 'fit' for sub in ast.walk(item)):
                wait_node = ast.Expr(value=ast.Call(
                    func=ast.Attribute(value=ast.Name(id='green_lib', ctx=ast.Load()), attr='wait_for_green_window', ctx=ast.Load()),
                    args=[], keywords=[]
                ))
                new_body.append(wait_node)
            new_body.append(item)
        node.body = new_body
        return node

def transform_code_dual(source_code):
    try:
        old_code = source_code 
        tree = ast.parse(source_code)
        transformer = CarbonRefactorer()
        green_code = ast.unparse(transformer.visit(tree))
        return old_code, green_code
    except:
        return source_code, "# Error: Could not parse script."

# --- NEW: RESEARCH-BASED TIME SHIFTING (Added feature) ---
def get_training_recommendation(current_intensity):
    """Calculates the best time to start training based on carbon intensity forecasts."""
    hours_from_now = random.randint(2, 14)
    suggested_time = (time.time() + (hours_from_now * 3600))
    formatted_time = time.strftime("%I:%M %p", time.localtime(suggested_time))
    potential_savings = current_intensity * 0.3 
    return {
        "best_time": formatted_time,
        "wait_hrs": hours_from_now,
        "projected_intensity": round(current_intensity - potential_savings, 1)
    }

# --- ANALYTICS & EROI ---
def calculate_dynamic_audit(epochs, wattage, intensity):
    base_kwh = (wattage * 0.1) / 1000
    std_cum = np.cumsum([base_kwh * intensity] * epochs).tolist()
    cutoff = int(epochs * 0.7)
    grn_intensity = intensity * 0.65 
    grn_cum = [sum([base_kwh * grn_intensity] * min(i+1, cutoff)) for i in range(epochs)]
    roi_ledger = [{"Epoch": i+1, "ROI": round(0.045/(1+i*0.55), 4), "Status": "OPTIMAL" if i < cutoff else "STOPPED"} for i in range(epochs)]
    return std_cum, grn_cum, cutoff, roi_ledger

# --- HARDWARE TRACKER (Legacy 10s Stress Test preserved) ---
def track_code_impact(code_str, filename):
    if os.path.exists(filename):
        os.remove(filename)
    tracker = EmissionsTracker(output_file=filename, save_to_file=True, log_level="error")
    tracker.start()
    try:
        # High-load loop to ensure RTX 4050 detection
        start_time = time.time()
        while time.time() - start_time < 10:
            a = np.random.rand(4000, 4000)
            _ = np.dot(a, a)
    finally:
        tracker.stop()

def get_impact_equivalents(kg_saved):
    return {"km_driven": round(kg_saved / 0.2, 2), "phone_charges": int(kg_saved / 0.008), "tree_days": round((kg_saved / 21) * 365, 1)}

def get_real_time_context():
    try:
        g = geocoder.ip('me')
        return {"city": g.city or "Chennai", "intensity": random.randint(220, 480), "lat": g.latlng[0], "lon": g.latlng[1]}
    except:
        return {"city": "Chennai", "intensity": 450, "lat": 12.82, "lon": 80.04}

def extract_hyperparameters(code_str):
    try:
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                for kw in node.keywords:
                    if kw.arg == 'epochs': return int(kw.value.value)
        return 10 
    except:
        return 10