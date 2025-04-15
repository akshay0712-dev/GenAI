import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

print('Vocab Size :\t', encoder.n_vocab) # 2,00,019 ~ 200k

text = "The cat sat on the mat."
text2 = "The mat sat on the cat."

# Tokenization
tokens = encoder.encode(text)
tokens2 = encoder.encode(text2)

print("Text :\t\t", text)
print("Text2 :\t\t", text2)
print("Encoded :\t", tokens) 
print("Encoded2 :\t", tokens2) 

# my_tokens = [976, 9059, 10139, 402, 290, 2450]

decoded = encoder.decode(encoder.encode(text))
decoded2 = encoder.decode(encoder.encode(text2))
print("Decoded :\t", decoded)
print("Decoded2 :\t", decoded2)