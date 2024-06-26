import numpy as np
from sentence_transformers import SentenceTransformer
from mlserver_huggingface.common import load_pipeline_from_settings
from mlserver_huggingface.runtime import HuggingFaceRuntime
from mlserver_huggingface.settings import HuggingFaceSettings
from mlserver.settings import ModelSettings


def test_sentence_transformers_pipeline():
    # A tiny sentence transformers model for testing, which only takes 17.6MB of memory
    pretrained_model = "sentence-transformers-testing/stsb-bert-tiny-safetensors"
    st_embeder = SentenceTransformer(pretrained_model)

    hf_settings = HuggingFaceSettings(
        pretrained_model=pretrained_model, task="sentence-embedding"
    )
    model_settings = ModelSettings(name="foo", implementation=HuggingFaceRuntime)
    pipeline = load_pipeline_from_settings(hf_settings, model_settings)
    sentences = [
        "This framework generates embeddings for each input sentence",
        "Sentences are passed as a list of string.",
        "The quick brown fox jumps over the lazy dog.",
    ]
    st_pred = st_embeder.encode(sentences)
    pipeline_pred = pipeline.predict(sentences)["embeddings"]
    assert np.array_equal(st_pred, pipeline_pred)
