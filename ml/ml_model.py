import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle


with open("C:/Users/hp/Desktop/RBL/project/Voice Email/voice_email/ml/Gmail_Int_Classification.pickle", "rb") as f:
    words_intent, inv_intent_dict = pickle.load(f)


model_intent = tf.keras.models.load_model(
    'C:/Users/hp/Desktop/RBL/project/Voice Email/voice_email/ml/Gmail_Intent_classification.model')


tokenizer_intent = Tokenizer(num_words=200, oov_token="<OOV>")
tokenizer_intent.fit_on_texts(words_intent)
word_index_intent = tokenizer_intent.word_index


def predict_intent(sentence):
    print("#################################################")
    sentence_list = [sentence]
    # Coverting words to no.
    sentence_sequence = tokenizer_intent.texts_to_sequences(sentence_list)
    predict = pad_sequences(sentence_sequence, maxlen=15, padding='post')

    predict_input = np.array(predict)
    # Since input array should have shape (1, 15)
    predict_input = predict.reshape(1, 15)
    # result = model_intent._make_predict_function(predict_input)

   
    result = model_intent.predict(predict_input)  # result shape here is
    # result = result.reshape(11)
    # print(result.shape)
    # Creating final output list
    final_output = []
    for i in result:

        # finding tag_no for the ith word in the input
        max_index = np.argmax(i)
        # Getting the tag_name for the corresponding tag_no.
        final_output.append(inv_intent_dict[max_index])
        if result[0][max_index] < 0.5:
            return 0

    return final_output




#           -----------------------            NER                      -----------------------

with open("C:/Users/hp/Desktop/RBL/project/Voice Email/voice_email/ml/Gmail_NER.pickle", "rb") as f:
    words_ner ,inv_ent_dict = pickle.load(f)

model_ner = tf.keras.models.load_model('C:/Users/hp/Desktop/RBL/project/Voice Email/voice_email/ml/Gmail_RNN.model')


tokenizer_ner = Tokenizer(num_words = 200, oov_token="<OOV>")
tokenizer_ner.fit_on_texts(words_ner)
word_index_ner = tokenizer_ner.word_index



def predict_entity(sentence):
    sentence_list = [sentence]
    sentence_sequence = tokenizer_ner.texts_to_sequences(sentence_list) #Coverting words to no.
    predict = pad_sequences(sentence_sequence, maxlen=15, padding='post')

    predict_input = np.array(predict)
    predict_input = predict.reshape(1,15)  #Since input array should have shape (1, 15)

    result = model_ner.predict(predict_input)  # result shape here is
    result = result.reshape(15, 6)

    #Creating final output list
    final_output = []
    for i in result:
        max_index = np.argmax(i) #finding tag_no for the ith word in the input
        final_output.append(inv_ent_dict[max_index]) #Getting the tag_name for the corresponding tag_no.

    return final_output
# print(predict_intent("open inbox"))
