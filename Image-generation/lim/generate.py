import torch
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",  # actively supported model
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)

prompt = "a cute futuristic robot playing guitar"
image = pipe(prompt).images[0]
image.save("output.png")
print("✅ Image saved as output.png")

