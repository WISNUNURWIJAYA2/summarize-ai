from transformers import MT5ForConditionalGeneration, models
from transformers import AutoTokenizer

MODEL_PATH = "models/MT5V6.2"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

print("Loading model...")
model = MT5ForConditionalGeneration.from_pretrained(
    MODEL_PATH
)

print("Model loaded successfully")


RATIO_CONFIG = {
    30: {
        "max_new_tokens": 100,
        "min_length": 30,
        "label": "RINGKAS (30%)"
    },
    50: {
        "max_new_tokens": 200,
        "min_length": 80,
        "label": "SEDANG (50%)"
    },
    80: {
        "max_new_tokens": 400,
        "min_length": 150,
        "label": "DETAIL (80%)"
    }
}


def summarize_text(text: str, ratio: int = 30):
    
#   Validate ratio
    if ratio not in RATIO_CONFIG:
        raise ValueError(
            f"Invalid ratio: {ratio}. Use 30, 50, or 80."
        )

    if not text.strip():
        raise ValueError(
            "Document contains no readable text."
        )

    cfg = RATIO_CONFIG[ratio]

    print("=" * 60)
    print("MODE :", cfg["label"])
    print("WORDS:", len(text.split()))
    print("=" * 60)

    chunks = []

    start = 0

    while start < len(text):
        chunks.append(
            text[start:start + 3000]
        )
        start += 2800

    summaries = []

    for idx, chunk in enumerate(chunks):

        print(
            f"Chunk {idx+1}/{len(chunks)}"
        )

        inputs = tokenizer(
            "summarize: " + chunk,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        )
        
# Debug Model Error
        try:
             
         outputs = model.generate(
                inputs["input_ids"],
                max_new_tokens=cfg["max_new_tokens"],
                min_length=cfg["min_length"],
                num_beams=4,
                no_repeat_ngram_size=3,
                repetition_penalty=1.2,
                do_sample=False,
                early_stopping=True
            )

        except Exception as e:

                raise RuntimeError(
                        f"Model generation failed: {str(e)}"
                )

        partial = tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        summaries.append(partial)

    final_summary = " ".join(
        summaries
    )

    print(
        "SUMMARY WORDS:",
        len(final_summary.split())
    )

    return final_summary