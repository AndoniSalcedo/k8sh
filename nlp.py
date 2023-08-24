import torch
from transformers import BertTokenizer, BertForMaskedLM

#model_name = "bert-base-uncased"
#tokenizer = BertTokenizer.from_pretrained(model_name)
#model = BertForMaskedLM.from_pretrained(model_name)

def syntax_correct(user_input):

    tokens = tokenizer.tokenize(user_input)
    masked_tokens = [token if token != '[UNK]' else '[MASK]' for token in tokens]

    # Generar predicciones
    inputs = tokenizer.convert_tokens_to_ids(masked_tokens)
    inputs = torch.tensor([inputs])
    with torch.no_grad():
        predictions = model(inputs)[0]

    # Obtener las palabras sugeridas por el modelo
    predicted_ids = torch.argmax(predictions, dim=-1)
    predicted_ids = predicted_ids.tolist()  # Convertir el tensor a lista
    predicted_tokens = tokenizer.convert_ids_to_tokens(predicted_ids)

    # Reemplazar los tokens '[MASK]' por las sugerencias
    corrected_tokens = []
    for token, suggested_token in zip(tokens, predicted_tokens):
        corrected_token = suggested_token if token == '[MASK]' else token
        corrected_tokens.append(corrected_token)

    # Postprocesamiento: Convertir tokens en un comando corregido
    corrected_command = ' '.join(corrected_tokens).replace(' ##', '').replace(' .', '.').replace(' ,', ',')
    return corrected_command

