# main.py
import os
import sys
from src.architect import refactor_script

def run_pipeline():
    print("="*40)
    print("[+] CARBON CUT: AI Refactoring Engine")
    print("="*40)

    input_file = "experiments/inputs/train_mnist.py"
    output_file = "experiments/outputs/train_mnist_green.py"

    # Step 1: Check Input
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    # Step 2: Refactor
    print(f"1. Reading dirty script: {input_file}...")
    refactor_script(input_file, output_file)

    # Step 3: Run the Green Script (Optional Auto-Run)
    print("\n2. Executing the NEW Green Script to demonstrate...")
    print("-" * 20)
    
    # We use os.system to run the generated file
    # Ensure the root dir is in pythonpath
    os.environ['PYTHONPATH'] = os.getcwd()
    os.system(f"python {output_file}")

if __name__ == "__main__":
    run_pipeline()
    import os

def generate_impact_report(dirty_model_path, green_model_path):
    print("\n" + "="*40)
    print("📊 FINAL CARBON IMPACT REPORT")
    print("="*40)
    
    if os.path.exists(dirty_model_path) and os.path.exists(green_model_path):
        dirty_size = os.path.getsize(dirty_model_path) / (1024 * 1024)
        green_size = os.path.getsize(green_model_path) / (1024 * 1024)
        
        reduction = ((dirty_size - green_size) / dirty_size) * 100
        
        print(f"Model Size (Standard): {dirty_size:.2f} MB")
        print(f"Model Size (Carbon Cut): {green_size:.2f} MB")
        print(f"📦 Storage/Inference Emission Reduction: {reduction:.2f}%")
        print("\nNote: Lower model size leads to fewer floating-point operations (FLOPs)")
        print("during inference, directly reducing processor power draw.")
    else:
        print("Error: Models not found for comparison.")

# Call this at the end of your run_pipeline() in main.py
# generate_impact_report("my_heavy_model.h5", "experiments/outputs/green_model.h5")