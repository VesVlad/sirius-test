from transformers import AutoModelWithLMHead, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained('./DockerRuDialoGPT-medium')
model = AutoModelWithLMHead.from_pretrained("./DockerRuDialoGPT-medium")

