import torch, pytest, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from train_cpu import MODEL   # import the model name constant

def test_model_name():
    assert "Qwen" in MODEL, "Model constant not as expected"

def test_import_no_cuda():
    assert not torch.cuda.is_available(), "CUDA should be disabled on CI"
