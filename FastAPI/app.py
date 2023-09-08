from fastapi import FastAPI
from model import tokenizer, model
import urllib
app = FastAPI()

def predict(text: str) -> str:
    inputs = tokenizer(text, return_tensors='pt')
    generated_token_ids = model.generate(
        **inputs,
        top_k=10,
        top_p=0.95,
        num_beams=3,
        num_return_sequences=1,
        do_sample=True,
        no_repeat_ngram_size=4,
        temperature=1.2,
        repetition_penalty=1.2,
        length_penalty=1.5,
        eos_token_id=50257,
        max_new_tokens=40
    )

    return tokenizer.decode(generated_token_ids[0])
@app.get("/api/{msg}")
async def read_request(msg: str):
    msg = urllib.parse.unquote(msg)
    return predict(msg)