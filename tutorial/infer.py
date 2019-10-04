#!/usr/bin/env python
# coding: utf-8

# In[24]:


import json
import gluonnlp as nlp
import mxnet as mx
from utils import predict_sentiment


# In[29]:


def model_fn(model_dir):
    """
    Load the gluon model. Called once when hosting service starts.
    :param: model_dir The directory where model files are stored.
    :return: a model (in this case a Gluon network)
    """
    prefix = 'checkpoint'
    net = mx.gluon.nn.SymbolBlock.imports(prefix + '-symbol.json',
                                          ['data0', 'data1', 'data2'],
                                          prefix + '-0000.params')
    net.load_parameters('%s/'%model_dir + prefix + '-0000.params', ctx=mx.cpu())
    vocab_json = open('%s/vocab.json'%model_dir).read()
    vocab = nlp.vocab.BERTVocab.from_json(vocab_json)
    return net, vocab


def transform_fn(model, data, input_content_type, output_content_type):
    """
    Transform a request using the Gluon model. Called once per request.
    :param net: The Gluon model.
    :param data: The request payload.
    :param input_content_type: The request content type.
    :param output_content_type: The (desired) response content type.
    :return: response payload and content type.
    """
    # we can use content types to vary input/output handling, but
    # here we just assume json for both                                                                                                      96,5          Bot
    net, vocabulary = model
    sentence = json.loads(data)
    tokenizer = nlp.data.BERTTokenizer(vocabulary)
    result = predict_sentiment(net, mx.cpu(), vocabulary, tokenizer, sentence)
    response_body = json.dumps(result)
    return response_body, output_content_type


# In[38]:


'''
# example usage:

model = model_fn('.')
data = json.dumps('this movie is great')
input_content_type = 'application/json'
output_content_type = 'application/json'
result, _ = transform_fn(model, data, input_content_type, output_content_type)
print(result)
'''

