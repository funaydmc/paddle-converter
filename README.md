# paddle-converter

Convert paddle model to onnx format automatically.

## Description

This tool converts all PaddlePaddle models (`.pdparams` files) in the `paddle/` directory to ONNX format and stores them in the `onnx/` directory with the same folder structure.

## Prerequisites

- Python 3.7 or higher
- PaddlePaddle
- paddle2onnx
- onnx

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Directory Structure

```
paddle-converter/
├── paddle/                      # Place your Paddle models here
│   ├── ppv1_lite_mobie/
│   │   ├── ppv1_lite_rec_mobie.pdparams
│   │   └── ppv1_lite_rec_mobie.pdmodel
│   └── other_models/
│       ├── model.pdparams
│       └── model.pdmodel
├── onnx/                        # ONNX models will be saved here (auto-created)
├── convert_paddle_to_onnx.py    # Conversion script
└── requirements.txt
```

## Usage

1. Place your Paddle model files (`.pdparams` and `.pdmodel`) in the `paddle/` directory with any folder structure you prefer.

2. Run the conversion script:

```bash
python convert_paddle_to_onnx.py
```

The script will:
- Recursively scan the `paddle/` directory for all `.pdparams` files
- Find corresponding `.pdmodel` files
- Convert each model to ONNX format
- Save the ONNX files in the `onnx/` directory with the same folder structure

## Example

Input:
```
paddle/ppv1_lite_mobie/ppv1_lite_rec_mobie.pdparams
paddle/ppv1_lite_mobie/ppv1_lite_rec_mobie.pdmodel
```

Output:
```
onnx/ppv1_lite_mobie/ppv1_lite_rec_mobie.onnx
```

## Notes

- Both `.pdparams` and `.pdmodel` files are required for conversion
- The script will skip any `.pdparams` file that doesn't have a corresponding `.pdmodel` file
- All output directories are created automatically
- Conversion progress and errors are logged to the console

