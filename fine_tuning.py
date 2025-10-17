from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

model_name = "meta-llama/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

prompt = "<|begin_of_text|><|start_header_id|>user<|end_header_id|>\nWho are you?<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"

response = pipe(prompt, max_new_tokens=100, temperature=0.7)
print(response[0]["generated_text"])
