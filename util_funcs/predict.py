from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
import tensorflow as tf

tokenizer = AutoTokenizer.from_pretrained("./EmoRoBERTa")
model = TFAutoModelForSequenceClassification.from_pretrained(
    "./EmoRoBERTa", from_pt=False  # ensure TF weights
)

counter = 0
def emotion_detection(text, progress_bar = None, total = None):
    global counter 
    counter += 1
    if progress_bar is not None and total is not None: 
        progress  = int((counter/total)*100)
        progress_bar.progress(progress, text=f"Processing: {counter}/{total}")
        # progress_placeholder.text(f"Processing Comment: {counter} / {total}")
    inputs = tokenizer(text, return_tensors="tf", truncation=True, padding=True)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = int(tf.math.argmax(logits, axis=-1)[0])
    labels = model.config.id2label
    return labels[predicted_class_id]