import pytest
import torch
from learn_former.model.submodels import (
    FeedForward,
    MultiHeadAttention,
    Embedding,
    PositionalEncoding,
    MaskGenerator,
)


#############################################
#### Test the feed forward layer ############
#############################################
def test_feedforward_layer(embedded_sentence: torch.Tensor):
    output_dim = 512
    ffm = FeedForward(input_dim=output_dim, hidden_dim=2048)
    x = ffm(embedded_sentence)
    assert x.shape == embedded_sentence.shape


def test_batch_feedforward_layer(embedded_sentence_batch: torch.Tensor):
    output_dim = 512
    ffm = FeedForward(input_dim=output_dim, hidden_dim=2048)
    x = ffm(embedded_sentence_batch)
    assert x.shape == (2, 10, output_dim)


#############################################
#### Test the multi-head attention layer ####
#############################################


def test_multiheadattention_layer(embedded_sentence: torch.Tensor):
    input_dim = 512
    num_heads = 8
    mha = MultiHeadAttention(input_dim=input_dim, num_heads=num_heads)

    x = mha(embedded_sentence, embedded_sentence, embedded_sentence)
    assert x.shape == (1, 10, input_dim)


def test_batch_multiheadattention_layer(embedded_sentence_batch: torch.Tensor):
    input_dim = 512
    num_heads = 8
    mha = MultiHeadAttention(input_dim=input_dim, num_heads=num_heads)

    x = mha(embedded_sentence_batch, embedded_sentence_batch, embedded_sentence_batch)
    assert x.shape == (2, 10, input_dim)


def test_multiheadattention_layer_with_mask(
    embedded_sentence: torch.Tensor, decoder_mask: torch.Tensor
):
    input_dim = 512
    num_heads = 8
    mha = MultiHeadAttention(input_dim=input_dim, num_heads=num_heads)

    x = mha(embedded_sentence, embedded_sentence, embedded_sentence, mask=decoder_mask)
    assert x.shape == (1, 10, input_dim)


def test_batch_multiheadattention_layer_with_mask(
    embedded_sentence_batch: torch.Tensor, decoder_mask_batch: torch.Tensor
):
    input_dim = 512
    num_heads = 8
    mha = MultiHeadAttention(input_dim=input_dim, num_heads=num_heads)

    x = mha(
        embedded_sentence_batch,
        embedded_sentence_batch,
        embedded_sentence_batch,
        mask=decoder_mask_batch,
    )
    assert x.shape == (2, 10, input_dim)


#############################################
#### Test the word embedding layer ##########
#############################################


def test_word_embedding_layer(tokenized_sentence: torch.Tensor):
    vocab_size = 10000
    embedding_dim = 512
    we = Embedding(vocab_size, embedding_dim)
    x = we(tokenized_sentence)

    token_shape = tokenized_sentence.shape
    assert x.shape == (token_shape[0], token_shape[1], embedding_dim)


def test_batch_word_embedding_layer(tokenized_sentence_batch: torch.Tensor):
    vocab_size = 10000
    embedding_dim = 512
    we = Embedding(vocab_size, embedding_dim)
    x = we(tokenized_sentence_batch)

    token_shape = tokenized_sentence_batch.shape
    assert x.shape == (token_shape[0], token_shape[1], embedding_dim)


#############################################
#### Test the positional encoding layer #####
#############################################


def test_positional_encoding_layer(embedded_sentence: torch.Tensor):
    max_len = 1024
    embedding_dims = 512
    pe = PositionalEncoding(max_len, embedding_dims)
    x = pe(embedded_sentence)
    assert x.shape == embedded_sentence.shape


def test_batch_positional_encoding_layer(embedded_sentence_batch: torch.Tensor):
    max_len = 1024
    embedding_dims = 512
    pe = PositionalEncoding(max_len, embedding_dims)
    x = pe(embedded_sentence_batch)
    assert x.shape == embedded_sentence_batch.shape


#############################################
#### Test the mask generator layer ##########
#############################################


def test_mask_generator_layer_without_lookahead(tokenized_sentence: torch.Tensor):

    padding_id = 7

    mg = MaskGenerator(padding_id)
    mask = mg(tokenized_sentence)
    assert mask.shape == (1, 1, 10, 10)


def test_mask_generator_layer_with_lookahead(tokenized_sentence: torch.Tensor):

    padding_id = 7

    mg = MaskGenerator(padding_id)
    mask = mg(tokenized_sentence, look_ahead=True)

    # The mask should be a lower triangular matrix
    # second element and all after this in first row should be 0
    assert torch.all(mask[:, :, 0, 1:] == 0)
