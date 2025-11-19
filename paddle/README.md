# Paddle Models Directory

Place your PaddlePaddle model files here for conversion to ONNX format.

## Required Files

For each model, you need both:
- `model_name.pdparams` - Model parameters file
- `model_name.pdmodel` - Model architecture file

## Example Structure

```
paddle/
├── ppv1_lite_mobie/
│   ├── ppv1_lite_rec_mobie.pdparams
│   └── ppv1_lite_rec_mobie.pdmodel
├── another_model/
│   ├── another_model.pdparams
│   └── another_model.pdmodel
└── single_file_model.pdparams
    single_file_model.pdmodel
```

After running the conversion script, the ONNX files will be saved in the `onnx/` directory with the same folder structure.
