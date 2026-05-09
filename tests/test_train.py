import os

def test_train_file_exists():
    assert os.path.exists("models/train.py")

    