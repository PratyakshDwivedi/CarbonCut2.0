# green_lib/pruner.py
import tensorflow as tf
import numpy as np
import os

def apply_pruning_and_save(model, filepath="experiments/outputs/green_model.keras"):
    print("\n[CarbonCut] ✂️ Phase 3: Manual Weight Pruning for Green Inference...")
    
    # Ensure directory exists
    output_dir = os.path.dirname(filepath)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not filepath.endswith('.keras'):
        filepath = filepath.replace('.h5', '.keras')

    try:
        # PURE RESEARCH LOGIC: Manual Sparsification
        # We zero out the bottom 50% of weights to reduce inference energy
        for layer in model.layers:
            if hasattr(layer, 'get_weights') and len(layer.get_weights()) > 0:
                weights = layer.get_weights()
                new_weights = []
                for w in weights:
                    # Only prune 2D weights (kernels), not biases
                    if len(w.shape) > 1:
                        threshold = np.percentile(np.abs(w), 50)
                        w_pruned = np.where(np.abs(w) < threshold, 0, w)
                        new_weights.append(w_pruned)
                    else:
                        new_weights.append(w)
                layer.set_weights(new_weights)
        
        model.save(filepath)
        print(f"[CarbonCut] ✅ SUCCESS: 50% Weights Zeroed for Sustainability.")
        print(f"[CarbonCut] Saved Green Model to: {filepath}")

    except Exception as e:
        print(f"[CarbonCut] ❌ Manual Pruning failed: {e}")
        model.save(filepath)