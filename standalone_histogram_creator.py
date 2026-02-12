#!/usr/bin/env python3
"""
Standalone Parquet to ROOT Histogram Creator
Creates pass/fail histograms for Tag-and-Probe efficiency measurements

Usage:
    python standalone_histogram_creator.py --config settings.py --flag passingCutBasedMedium122XV1
"""

import os
import sys
import glob
import argparse

# Check if we can import pandas outside of CMSSW environment
try:
    import pandas as pd
    import numpy as np
    import uproot
    from pathlib import Path
    PANDAS_AVAILABLE = True
    print("✓ pandas/uproot available - using modern parquet reading")
except ImportError as e:
    PANDAS_AVAILABLE = False
    print(f"✗ pandas/uproot not available: {e}")
    print("This script requires pandas and uproot. Try running outside CMSSW environment.")
    sys.exit(1)

def apply_base_selection(df, cut_expression):
    """
    Apply base selection cuts to the DataFrame
    
    Args:
        df: pandas DataFrame with parquet data
        cut_expression: string expression for base cuts (e.g., 'tag_Ele_pt > 35 && abs(tag_Ele_eta) < 2.17')
    
    Returns:
        pandas DataFrame with base selection applied
    """
    print(f"Applying base selection: {cut_expression}")
    
    if not cut_expression or cut_expression.strip() == "":
        print("  No base selection specified")
        return df
    
    initial_events = len(df)
    
    # Convert C++ style operators to pandas equivalents
    pandas_expr = cut_expression.replace('&&', '&').replace('||', '|').replace('abs(', 'np.abs(')
    
    # Common variable name mapping for TnP
    var_mapping = {
        'tag_Ele_pt': 'tag_Ele_pt',
        'tag_Ele_eta': 'tag_Ele_eta', 
        'el_q': 'el_q',
        'tag_Ele_q': 'tag_Ele_q',
        'el_pt': 'el_pt',
        'el_eta': 'el_eta',
        'pair_mass': 'pair_mass'
    }
    
    # Check which variables are available
    available_vars = []
    missing_vars = []
    
    for var in var_mapping.keys():
        if var in pandas_expr:
            if var_mapping[var] in df.columns:
                available_vars.append(var)
            else:
                missing_vars.append(var)
    
    if missing_vars:
        print(f"  Warning: Missing variables in DataFrame: {missing_vars}")
        print(f"  Available columns: {list(df.columns)}")
        print("  Skipping base selection")
        return df
    
    try:
        # Apply the selection
        print(f"  Evaluating: {pandas_expr}")
        mask = df.eval(pandas_expr)
        df_selected = df[mask].copy()
        
        final_events = len(df_selected)
        selection_efficiency = final_events / initial_events * 100
        
        print(f"  Base selection: {initial_events} → {final_events} events ({selection_efficiency:.2f}%)")
        
        return df_selected
        
    except Exception as e:
        print(f"  Error applying base selection: {e}")
        print(f"  Skipping base selection and using all events")
        return df


def evaluate_flag_condition(df, flag_expression, flag_name):
    """
    Evaluate the flag condition on the DataFrame
    
    Args:
        df: pandas DataFrame with parquet data
        flag_expression: string expression to evaluate (e.g., '(passingCutBasedMedium122XV1 == 1)')
        flag_name: name of the flag for debugging
    
    Returns:
        numpy array of boolean values (True = pass, False = fail)
    """
    print(f"Evaluating flag '{flag_name}': {flag_expression}")
    
    # Map common flag names to actual column names in the Parquet files
    flag_mapping = {
        'passingCutBasedMedium122XV1': 'medium',
        'passingCutBasedTight122XV1': 'tight', 
        'passingCutBasedLoose122XV1': 'loose',
        'passingVeto': 'veto',
        'passingMedium': 'medium',
        'passingTight': 'tight',
        'passingLoose': 'loose'
    }
    
    # Check if this is a mapped flag
    if flag_name in flag_mapping:
        actual_column = flag_mapping[flag_name]
        if actual_column in df.columns:
            print(f"  Mapped '{flag_name}' → '{actual_column}' column")
            result = (df[actual_column] == 1).values
            print(f"  Found {np.sum(result)} passing events out of {len(result)} total")
            return result
    
    # For simple boolean flags like '(passingCutBasedMedium122XV1 == 1)'
    if '==' in flag_expression:
        # Extract column name from expression like '(columnName == 1)'
        import re
        match = re.search(r'\((\w+)\s*==\s*(\d+)\)', flag_expression)
        if match:
            column_name = match.group(1)
            expected_value = int(match.group(2))
            
            # Check if mapped column exists
            if column_name in flag_mapping and flag_mapping[column_name] in df.columns:
                actual_column = flag_mapping[column_name]
                print(f"  Mapped '{column_name}' → '{actual_column}' column")
                result = (df[actual_column] == expected_value).values
                print(f"  Found {np.sum(result)} passing events out of {len(result)} total")
                return result
            elif column_name in df.columns:
                result = (df[column_name] == expected_value).values
                print(f"  Found {np.sum(result)} passing events out of {len(result)} total")
                return result
    
    # For complex MVA cuts with && and || operators
    if 'probe_Ele_nonTrigMVA' in flag_expression or 'tag_Ele' in flag_expression:
        print("  Complex MVA expression - evaluating with pandas.eval()")
        # Replace C++ style operators with pandas equivalents
        pandas_expr = flag_expression.replace('&&', '&').replace('||', '|')
        # Map column names in the expression
        for old_name, new_name in flag_mapping.items():
            pandas_expr = pandas_expr.replace(old_name, new_name)
        
        try:
            result = df.eval(pandas_expr).values
            print(f"  Found {np.sum(result)} passing events out of {len(result)} total")
            return result
        except Exception as e:
            print(f"  Error in MVA evaluation: {e}")
    
    # Generic evaluation using pandas eval
    try:
        # Apply column mapping to the expression
        mapped_expr = flag_expression
        for old_name, new_name in flag_mapping.items():
            mapped_expr = mapped_expr.replace(old_name, new_name)
        
        result = df.eval(mapped_expr).values
        print(f"  Found {np.sum(result)} passing events out of {len(result)} total")
        return result
    except Exception as e:
        print(f"  Error evaluating expression: {e}")
        print(f"  Available columns: {list(df.columns)}")
        print("  Suggestion: Use column names like 'medium', 'tight', 'loose', 'veto'")
        return np.zeros(len(df), dtype=bool)

def create_histograms_for_bins(df, kinematic_bins, flag_expression, flag_name, output_dir, output_file_path=None):
    """
    Create pass/fail histograms for each kinematic bin
    
    Args:
        df: pandas DataFrame with parquet data
        kinematic_bins: dictionary of kinematic binning
        flag_expression: string expression for pass/fail evaluation
        flag_name: name of the flag
        output_dir: directory to save ROOT histograms
    """
    import ROOT
    
    # Evaluate pass/fail condition
    pass_mask = evaluate_flag_condition(df, flag_expression, flag_name)
    
    # Define invariant mass range and bins for fitting
    mass_min, mass_max = 60, 120  # GeV for Z → ee
    mass_bins = 60
    
    # Create output ROOT file - use specified path or default naming
    if output_file_path:
        output_file = output_file_path
    else:
        # Fallback to old naming scheme
        sample_name = "data_Run3_2025_C"  
        output_file = f"{output_dir}/{sample_name}_{flag_name}.root"
    
    root_file = ROOT.TFile(output_file, "RECREATE")
    
    # Get kinematic variables
    pt_bins = kinematic_bins['pt']
    eta_bins = kinematic_bins['eta']
    
    total_bins_created = 0
    bin_counter = 0  # Sequential bin numbering
    
    print(f"\nCreating histograms for {len(pt_bins)-1} pT bins × {len(eta_bins)-1} eta bins")
    
    # Loop over pT and eta bins
    for i_pt in range(len(pt_bins)-1):
        pt_min, pt_max = pt_bins[i_pt], pt_bins[i_pt+1]
        
        for i_eta in range(len(eta_bins)-1):
            eta_min, eta_max = eta_bins[i_eta], eta_bins[i_eta+1]
            
            # Define bin selection
            bin_mask = (
                (df['el_pt'] >= pt_min) & 
                (df['el_pt'] < pt_max) & 
                (df['el_eta'] >= eta_min) & 
                (df['el_eta'] < eta_max)
            )
            
            n_events_bin = np.sum(bin_mask)
            if n_events_bin < 10:  # Skip bins with too few events
                continue
                
            # Get invariant mass for this bin
            mass_values = df[bin_mask]['pair_mass'].values
            weights = df[bin_mask].get('totWeight', pd.Series(np.ones(n_events_bin))).values
            
            # If totWeight column doesn't exist, use unit weights
            if 'totWeight' not in df.columns:
                weights = np.ones(n_events_bin)
            
            # Separate pass and fail events
            pass_events_bin = bin_mask & pass_mask
            fail_events_bin = bin_mask & (~pass_mask)
            
            n_pass = np.sum(pass_events_bin)
            n_fail = np.sum(fail_events_bin)
            
            print(f"  Bin pT=[{pt_min:.1f},{pt_max:.1f}], eta=[{eta_min:.2f},{eta_max:.2f}]: {n_pass} pass, {n_fail} fail")
            
            if n_pass < 5 and n_fail < 5:  # Skip bins with very few events
                continue
            
            # Create bin names following exact TnP convention: bin{XX}_{descriptive_name}
            # Format: bin{zero-padded}_el_eta_{eta_range}_el_pt_{pt_range} (eta before pt!)
            descriptive_name = f"el_eta"
            if eta_min < 0:
                descriptive_name += f"_m{abs(eta_min):.2f}To".replace('.', 'p')
            else:
                descriptive_name += f"_{eta_min:.2f}To".replace('.', 'p')
            if eta_max < 0:
                descriptive_name += f"m{abs(eta_max):.2f}".replace('.', 'p')
            else:
                descriptive_name += f"{eta_max:.2f}".replace('.', 'p')
            descriptive_name += f"_el_pt_{pt_min:.0f}p00To{pt_max:.0f}p00"
            
            # Standard TnP format: bin{XX}_{descriptive}_Pass/Fail
            bin_name = f"bin{bin_counter:02d}_{descriptive_name}"
            
            # Pass histogram - following exact TnP format: bin{XX}_{descriptive}_Pass
            hist_pass_name = f"{bin_name}_Pass"
            hist_pass = ROOT.TH1D(hist_pass_name, f"Pass: {flag_name} {bin_name}", 
                                 mass_bins, mass_min, mass_max)
            
            # Fill pass histogram
            if n_pass > 0:
                mass_pass = df[pass_events_bin]['pair_mass'].values
                # For TnP fitting, avoid using weights to prevent sum-of-weights issues
                # Fill histogram with unit weights only
                for mass in mass_pass:
                    hist_pass.Fill(mass)
            
            # Fail histogram - following exact TnP format: bin{XX}_{descriptive}_Fail 
            hist_fail_name = f"{bin_name}_Fail"
            hist_fail = ROOT.TH1D(hist_fail_name, f"Fail: {flag_name} {bin_name}", 
                                 mass_bins, mass_min, mass_max)
            
            # Fill fail histogram
            if n_fail > 0:
                mass_fail = df[fail_events_bin]['pair_mass'].values
                # For TnP fitting, avoid using weights to prevent sum-of-weights issues
                # Fill histogram with unit weights only
                for mass in mass_fail:
                    hist_fail.Fill(mass)
            
            # Write histograms to file
            hist_pass.Write()
            hist_fail.Write()
            
            total_bins_created += 1
            bin_counter += 1  # Increment for next bin
    
    root_file.Close()
    print(f"\n✓ Created {total_bins_created} kinematic bins with pass/fail histograms")
    print(f"✓ Histograms saved to: {output_file}")

def load_config_file(config_path):
    """Load configuration file and extract flags and binning"""
    
    # Add the config directory to Python path
    config_dir = os.path.dirname(config_path)
    if config_dir not in sys.path:
        sys.path.insert(0, config_dir)
    
    # Import the config module
    config_name = os.path.basename(config_path).replace('.py', '')
    config_module = __import__(config_name)
    
    # Extract flags
    flags = getattr(config_module, 'flags', {})
    
    # Extract kinematic binning from biningDef (TnP framework standard)
    bining_def = getattr(config_module, 'biningDef', None)
    
    if bining_def:
        # Convert biningDef format to our format
        kinematic_bins = {}
        for bin_def in bining_def:
            var_name = bin_def['var']
            if var_name in ['el_pt', 'pt']:
                kinematic_bins['pt'] = bin_def['bins']
            elif var_name in ['el_eta', 'el_sc_eta', 'eta']:
                kinematic_bins['eta'] = bin_def['bins']
        
        print(f"Using binning from config: pt={len(kinematic_bins.get('pt', []))-1} bins, eta={len(kinematic_bins.get('eta', []))-1} bins")
    else:
        # Fallback to standard electron binning if no biningDef found
        kinematic_bins = getattr(config_module, 'binning', {
            'pt': [10, 15, 20, 25, 30, 35, 40, 50, 60, 80, 100, 200],
            'eta': [-2.5, -2.0, -1.566, -1.444, -0.8, 0.0, 0.8, 1.444, 1.566, 2.0, 2.5]
        })
        print("Warning: No biningDef found in config, using fallback binning")
    
    # Extract parquet file patterns and config
    parquet_pattern = getattr(config_module, 'parquet_pattern', None)
    parquet_config = getattr(config_module, 'parquet_config', {})
    
    # Extract base selection cuts
    cut_base = getattr(config_module, 'cutBase', None)
    
    return flags, kinematic_bins, parquet_pattern, parquet_config, cut_base

def main():
    parser = argparse.ArgumentParser(description='Create pass/fail histograms from Parquet files')
    parser.add_argument('--config', required=True, help='Configuration file path')
    parser.add_argument('--flag', required=True, help='Flag to process')
    parser.add_argument('--output', default='./results', help='Base output directory')
    parser.add_argument('--pattern', help='Parquet file pattern (overrides config)')
    parser.add_argument('--campaign', default='Run3_2025_C', help='Campaign name for directory structure')
    parser.add_argument('--analysis', default='tnpEleID', help='Analysis type (tnpEleID, tnpPhoID, etc.)')
    parser.add_argument('--sample-type', default='data', choices=['data', 'mc'], help='Sample type: data or mc')
    
    args = parser.parse_args()
    
    # Load configuration
    flags, kinematic_bins, parquet_pattern, parquet_config, cut_base = load_config_file(args.config)
    
    # Check if flag exists
    if args.flag not in flags:
        print(f"Error: Flag '{args.flag}' not found in configuration")
        print(f"Available flags: {list(flags.keys())}")
        return 1
    
    flag_expression = flags[args.flag]
    print(f"Processing flag '{args.flag}' with expression: {flag_expression}")
    
    # Use pattern from command line or config, considering sample type
    if args.pattern:
        parquet_pattern = args.pattern
    else:
        # Select the appropriate pattern based on sample type
        if args.sample_type == 'data':
            if 'data_input_files' in parquet_config:
                parquet_pattern = f"{parquet_config['data_input_files']}/*.parquet"
            else:
                parquet_pattern = parquet_pattern  # fallback to original
        else:  # mc
            if 'mc_input_files' in parquet_config:
                parquet_pattern = f"{parquet_config['mc_input_files']}/*.parquet"
            else:
                print("Error: MC input files not specified in parquet_config['mc_input_files']")
                return 1
    
    if not parquet_pattern:
        print("Error: No parquet file pattern specified")
        return 1
    
    print(f"Sample type: {args.sample_type}")
    print(f"Looking for Parquet files matching: {parquet_pattern}")
    
    # Find Parquet files
    parquet_files = glob.glob(parquet_pattern)
    if not parquet_files:
        print(f"Error: No Parquet files found matching pattern: {parquet_pattern}")
        return 1
    
    print(f"Found {len(parquet_files)} Parquet files")
    
    # Create output directory following TnP structure: results/{campaign}/{analysis}/{flag}/
    output_dir = f"{args.output}/{args.campaign}/{args.analysis}/{args.flag}"
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory: {output_dir}")
    
    # Load and combine all Parquet files
    print("Loading Parquet files...")
    dfs = []
    for pf in parquet_files[:5]:  # Limit to first 5 files for testing
        print(f"  Reading {pf}")
        df = pd.read_parquet(pf)
        dfs.append(df)
    
    # Combine all data
    df_combined = pd.concat(dfs, ignore_index=True)
    print(f"Loaded {len(df_combined)} total events")
    print(f"Columns available: {list(df_combined.columns)}")
    
    # Apply base selection cuts if specified
    if cut_base:
        print(f"\nApplying base selection from config: {cut_base}")
        df_combined = apply_base_selection(df_combined, cut_base)
        print(f"After base selection: {len(df_combined)} events")
    else:
        print("\nNo base selection specified in config - using all events")
    
    # Create histograms
    # Determine the correct output filename based on sample type
    if args.sample_type == 'data':
        output_filename = f"data_{args.campaign}_{args.flag}.root"
    else:  # mc
        output_filename = f"mc_{args.campaign}_{args.flag}.root"
    
    output_file_path = f"{output_dir}/{output_filename}"
    
    create_histograms_for_bins(df_combined, kinematic_bins, flag_expression, args.flag, output_dir, output_file_path)
    
    return 0
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

def create_tnp_histograms(input_path, output_file, flag_column, eta_bins, pt_bins, mass_range, n_mass_bins, force_recreate=False):
    """
    Public interface to create TnP histograms from Parquet files
    
    Args:
        input_path: Path to directory containing Parquet files
        output_file: Path to output ROOT file
        flag_column: Column name for pass/fail flag (e.g., 'medium', 'tight')
        eta_bins: List of eta bin edges
        pt_bins: List of pt bin edges  
        mass_range: Tuple of (mass_min, mass_max) for histograms
        n_mass_bins: Number of mass bins
        force_recreate: Whether to recreate histograms even if output file exists
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Check if output file already exists
        if os.path.exists(output_file) and not force_recreate:
            print(f"✅ Histogram file already exists: {output_file}")
            print(f"   Skipping creation. Use force_recreate=True to overwrite.")
            return True
        elif force_recreate and os.path.exists(output_file):
            print(f"🔄 Force recreate enabled - will overwrite existing file: {output_file}")
        
        import glob
        
        # Find Parquet files
        parquet_files = glob.glob(f"{input_path}/*.parquet")
        if not parquet_files:
            print(f"No Parquet files found in {input_path}")
            return False
            
        print(f"Found {len(parquet_files)} Parquet files")
        
        # Read Parquet files (limit for testing)
        dfs = []
        for pf in parquet_files[:5]:  # Limit to first 5 files for testing
            print(f"  Reading {pf}")
            df = pd.read_parquet(pf)
            dfs.append(df)
        
        # Combine data
        df_combined = pd.concat(dfs, ignore_index=True)
        print(f"Loaded {len(df_combined)} total events")
        
        # Setup kinematic bins
        kinematic_bins = {
            'eta': eta_bins,
            'pt': pt_bins
        }
        
        # Flag expression - simple boolean check
        flag_expression = f"({flag_column} == 1)"
        
        # Create output directory
        output_dir = os.path.dirname(output_file)
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract flag name from output file  
        flag_name = os.path.basename(output_file).split('_')[-1].replace('.root', '')
        
        # Create histograms
        create_histograms_for_bins(df_combined, kinematic_bins, flag_expression, flag_name, os.path.dirname(output_file), output_file)
        
        return True
        
    except Exception as e:
        print(f"Error creating TnP histograms: {e}")
        import traceback
        traceback.print_exc()
        return False
