# src/architect.py
import ast
import astunparse # You might need: pip install astunparse

class CarbonArchitect(ast.NodeTransformer):
    """
    Parses Python code and injects CarbonCut logic.
    """
    
    def visit_Import(self, node):
        return node

    # 1. Inject Imports at the top
    def visit_Module(self, node):
        # Add imports for our green lib
        green_imports = ast.parse(
            "from green_lib.scheduler import GridScheduler\n"
            "from green_lib.governor import EROIGovernor\n"
            "from green_lib.pruner import apply_pruning_and_save"
        ).body
        
        # Insert at the top of the file
        node.body = green_imports + node.body
        self.generic_visit(node)
        return node

    # 2. Inject Scheduler before 'model.fit'
    # 3. Inject Governor inside 'model.fit'
    def visit_Expr(self, node):
        # Look for model.fit()
        if isinstance(node.value, ast.Call) and \
           isinstance(node.value.func, ast.Attribute) and \
           node.value.func.attr == 'fit':
            
            # PHASE 1 INJECTION: Add Grid Check before this line
            grid_check_code = ast.parse("GridScheduler().wait_for_green_window()").body[0]
            
            # PHASE 2 INJECTION: Add Callback
            # Check if callbacks keyword exists, if not create it
            callback_keyword = None
            for kw in node.value.keywords:
                if kw.arg == 'callbacks':
                    callback_keyword = kw
                    break
            
            gov_call = ast.parse("EROIGovernor()").body[0].value
            
            if callback_keyword:
                # Append to existing list
                callback_keyword.value.elts.append(gov_call)
            else:
                # Create new callbacks list
                new_kw = ast.keyword(arg='callbacks', value=ast.List(elts=[gov_call], ctx=ast.Load()))
                node.value.keywords.append(new_kw)

            # Return a list: [GridCheck, ModelFit]
            return [grid_check_code, node]

        # PHASE 3 INJECTION: Look for model.save()
        if isinstance(node.value, ast.Call) and \
           isinstance(node.value.func, ast.Attribute) and \
           node.value.func.attr == 'save':
            
            # Replace model.save() with apply_pruning_and_save(model)
            model_name = node.value.func.value # Get the variable name of the model
            
            # Create the new function call node
            new_node = ast.Expr(
                value=ast.Call(
                    func=ast.Name(id='apply_pruning_and_save', ctx=ast.Load()),
                    args=[model_name],
                    keywords=[ast.keyword(arg='filepath', value=node.value.args[0])]
                )
            )
            return new_node

        return node

def refactor_script(input_path, output_path):
    with open(input_path, "r") as f:
        tree = ast.parse(f.read())
    
    # Run the Transformer
    optimizer = CarbonArchitect()
    new_tree = optimizer.visit(tree)
    ast.fix_missing_locations(new_tree)
    
    # Write the new code
    with open(output_path, "w") as f:
        f.write(astunparse.unparse(new_tree))
    
    print(f"✨ Transformation Complete! Green script saved to: {output_path}")
    # src/architect.py
import ast
import astunparse
import os  # <--- Make sure this import is at the top!

# ... (keep all your existing CarbonArchitect class code here) ...

def refactor_script(input_path, output_path):
    with open(input_path, "r") as f:
        tree = ast.parse(f.read())
    
    # Run the Transformer
    optimizer = CarbonArchitect()
    new_tree = optimizer.visit(tree)
    ast.fix_missing_locations(new_tree)
    
    # --- ADD THIS LOGIC HERE ---
    # Get the directory name (experiments/outputs)
    output_dir = os.path.dirname(output_path)
    # Create the directory if it doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # ---------------------------

    # Write the new code
    with open(output_path, "w") as f:
        f.write(astunparse.unparse(new_tree))
    
    print(f"Transformation Complete! Green script saved to: {output_path}")