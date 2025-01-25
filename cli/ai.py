import torch
from transformers import MllamaForConditionalGeneration, AutoProcessor

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    # device_map="auto",
)

def make_request(prompt, image=None):
    processor = AutoProcessor.from_pretrained(model_id)

    num_images = 0
    # if it is a pillow image
    if image and hasattr(image, "size"):
        num_images = 1
    elif image and hasattr(image[0], "size"):
        num_images = len(image)

    messages = [
        {"role": "user", "content": [
            {"type": "text", "text": prompt}
        ]}
    ]

    for _ in range(num_images):
        messages[0]["content"].append({"type": "image"})

    input_text = processor.apply_chat_template(messages, add_generation_prompt=True)

    if image:
        inputs = processor(
            image,
            input_text,
            add_special_tokens=False,
            return_tensors="pt",
        ).to(model.device)
    else:
        inputs = processor(
            None,
            input_text,
            add_special_tokens=False,
            return_tensors="pt",
        ).to(model.device)

    output = model.generate(**inputs, max_new_tokens=30)
    return processor.decode(output[0], skip_special_tokens=True).split("assistant\n", 1)[1].strip()
