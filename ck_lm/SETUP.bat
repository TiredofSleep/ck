@echo off
echo === CK-LM Environment Setup ===
echo Installs CUDA PyTorch + Unsloth for living CK training
echo Requires: Python 3.13, RTX 4070 (CUDA 12.x)
echo.

set PYTHON=C:\Users\brayd\AppData\Local\Programs\Python\Python313\python.exe

echo [1/4] Uninstalling CPU torch...
%PYTHON% -m pip uninstall torch torchvision torchaudio -y

echo [2/4] Installing CUDA 12.1 torch (fits RTX 4070)...
%PYTHON% -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo [3/4] Installing Unsloth + training stack...
%PYTHON% -m pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
%PYTHON% -m pip install transformers datasets peft trl accelerate bitsandbytes

echo [4/4] Verifying CUDA...
%PYTHON% -c "import torch; print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0)); print('VRAM:', round(torch.cuda.get_device_properties(0).total_memory/1e9,1), 'GB')"

echo.
echo Setup complete. Run: python ck_lm\ck_field_layer.py to test field geometry.
pause
