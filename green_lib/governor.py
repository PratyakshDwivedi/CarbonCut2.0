
import tensorflow as tf
import time

class EROIGovernor(tf.keras.callbacks.Callback):
    def __init__(self, patience=2, min_roi=0.001):
        super(EROIGovernor, self).__init__()
        self.patience = patience
        self.min_roi = min_roi
        self.wait = 0
        self.best_acc = 0.0
        self.start_time = 0

    def on_epoch_begin(self, epoch, logs=None):
        self.start_time = time.time()

    def on_epoch_end(self, epoch, logs=None):
        current_acc = logs.get('accuracy')
        if not current_acc: return

       
        elapsed_time = time.time() - self.start_time
        
        # Calculate ROI: (Gain in Accuracy) / (Cost in Time/Energy)
        accuracy_gain = current_acc - self.best_acc
        
        # Avoid division by zero
        roi = accuracy_gain / (elapsed_time + 1e-7)

        print(f"\n[CarbonCut] Epoch {epoch+1}: Accuracy={current_acc:.4f}, ROI={roi:.6f}")

        if roi < self.min_roi and epoch > 0:
            self.wait += 1
            if self.wait >= self.patience:
                print(f"\n[CarbonCut] 🛑 CUT DETECTED: Energy ROI too low. Stopping training to save carbon.")
                self.model.stop_training = True
        else:
            self.wait = 0
            
        if current_acc > self.best_acc:
            self.best_acc = current_acc