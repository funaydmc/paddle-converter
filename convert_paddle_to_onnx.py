#!/usr/bin/env python3
"""
Paddle to ONNX Converter Script

This script converts all Paddle model files (.pdparams) in the paddle/ directory
to ONNX format and stores them in the onnx/ directory with the same folder structure.

Example:
    /paddle/ppv1_lite_mobie/ppv1_lite_rec_mobie.pdparams
    -> /onnx/ppv1_lite_mobie/ppv1_lite_rec_mobie.onnx
"""

import os
import sys
from pathlib import Path
import logging

try:
    import paddle2onnx
    import paddle
except ImportError as e:
    print(f"Error: Required dependencies not installed. Please run: pip install -r requirements.txt")
    print(f"Import error: {e}")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def find_pdparams_files(paddle_dir):
    """
    Recursively find all .pdparams files in the paddle directory.
    
    Args:
        paddle_dir (Path): Path to the paddle directory
        
    Returns:
        list: List of Path objects for all .pdparams files
    """
    pdparams_files = []
    
    if not paddle_dir.exists():
        logger.warning(f"Paddle directory not found: {paddle_dir}")
        return pdparams_files
    
    for pdparams_file in paddle_dir.rglob("*.pdparams"):
        pdparams_files.append(pdparams_file)
        
    return pdparams_files


def get_output_path(pdparams_file, paddle_dir, onnx_dir):
    """
    Generate the output ONNX file path based on the input .pdparams file.
    
    Args:
        pdparams_file (Path): Path to the input .pdparams file
        paddle_dir (Path): Base paddle directory
        onnx_dir (Path): Base onnx directory
        
    Returns:
        Path: Output path for the ONNX file
    """
    # Get relative path from paddle_dir
    relative_path = pdparams_file.relative_to(paddle_dir)
    
    # Change extension to .onnx
    onnx_relative_path = relative_path.with_suffix('.onnx')
    
    # Create full output path
    output_path = onnx_dir / onnx_relative_path
    
    return output_path


def convert_paddle_to_onnx(pdparams_file, pdmodel_file, output_path):
    """
    Convert a Paddle model to ONNX format.
    
    Args:
        pdparams_file (Path): Path to the .pdparams file
        pdmodel_file (Path): Path to the .pdmodel file
        output_path (Path): Path where the ONNX file will be saved
        
    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read Paddle model
        with open(pdmodel_file, 'rb') as f:
            model_content = f.read()
        
        with open(pdparams_file, 'rb') as f:
            params_content = f.read()
        
        # Convert to ONNX
        logger.info(f"Converting {pdparams_file.name} to ONNX...")
        onnx_model = paddle2onnx.convert(
            model_content=model_content,
            params_content=params_content,
            save_file=str(output_path),
            opset_version=11
        )
        
        if onnx_model or output_path.exists():
            logger.info(f"Successfully converted: {output_path}")
            return True
        else:
            logger.error(f"Conversion failed: {pdparams_file}")
            return False
            
    except Exception as e:
        logger.error(f"Error converting {pdparams_file}: {str(e)}")
        return False


def main():
    """
    Main function to convert all Paddle models to ONNX format.
    """
    # Get the script directory
    script_dir = Path(__file__).parent.resolve()
    
    # Define directories
    paddle_dir = script_dir / "paddle"
    onnx_dir = script_dir / "onnx"
    
    logger.info("=" * 60)
    logger.info("Paddle to ONNX Converter")
    logger.info("=" * 60)
    logger.info(f"Paddle directory: {paddle_dir}")
    logger.info(f"ONNX directory: {onnx_dir}")
    logger.info("=" * 60)
    
    # Find all .pdparams files
    pdparams_files = find_pdparams_files(paddle_dir)
    
    if not pdparams_files:
        logger.warning(f"No .pdparams files found in {paddle_dir}")
        logger.info("Please ensure your Paddle models are in the 'paddle/' directory")
        return
    
    logger.info(f"Found {len(pdparams_files)} .pdparams file(s)")
    
    # Convert each file
    success_count = 0
    failed_count = 0
    
    for pdparams_file in pdparams_files:
        # Look for corresponding .pdmodel file
        pdmodel_file = pdparams_file.with_suffix('.pdmodel')
        
        if not pdmodel_file.exists():
            logger.warning(f"Skipping {pdparams_file.name}: No corresponding .pdmodel file found")
            failed_count += 1
            continue
        
        # Get output path
        output_path = get_output_path(pdparams_file, paddle_dir, onnx_dir)
        
        # Convert
        if convert_paddle_to_onnx(pdparams_file, pdmodel_file, output_path):
            success_count += 1
        else:
            failed_count += 1
    
    # Summary
    logger.info("=" * 60)
    logger.info("Conversion Summary")
    logger.info("=" * 60)
    logger.info(f"Total files: {len(pdparams_files)}")
    logger.info(f"Successfully converted: {success_count}")
    logger.info(f"Failed: {failed_count}")
    logger.info("=" * 60)
    
    if success_count > 0:
        logger.info(f"ONNX models saved in: {onnx_dir}")


if __name__ == "__main__":
    main()
