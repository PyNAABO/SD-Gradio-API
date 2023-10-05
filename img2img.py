import json
import base64
import requests
from PIL import Image
from io import BytesIO

headers = {'accept': 'application/json', 'Content-Type': 'application/json'}


def get_size(image_path):
    with Image.open(image_path) as img:
        try:
            width, height = img.size
            if width > 1080 and height > 1080:
                return width / 2, height / 2
            else:
                return width, height
        except Exception as e:
            print(f"Error: {e}")
            width, height = img.size
            return width, height


def process_image(image_path):
    # Open and read the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Read the binary data of the image
        image_binary = image_file.read()

    # Encode the binary data to Base64
    image_base64 = base64.b64encode(image_binary).decode("utf-8")
    return f"data:image/png;base64,{image_base64}"
    # return {"image": f"data:image/png;base64,{image_base64}"}


def img2img(
        url,
        image_path="./output_image.png",
        prompt="Anime Style, highly detailed",
        steps=20,  # Adjust the number of steps as needed
        cfg_scale=7.5,  # Adjust the scale as needed
        seed=-1):  # Adjust the seed as needed
    url = f"{url}sdapi/v1/img2img"
    width, height = get_size(image_path)
    print(width, height)
    payload = json.dumps({
        "prompt": prompt,
        "styles": ["photorealistic", "cartoonish",
                   "abstract"],  # Experiment with styles
        "seed": seed,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height,
        "restore_faces": True,
        "tiling": False,
        "do_not_save_samples": True,
        "do_not_save_grid": False,
        "denoising_strength": 0.505,  # Adjust denoising strength
        "init_images":
        [process_image(image_path)],  # Use your input image as an initial seed
        "resize_mode": 0,
        "image_cfg_scale": 10,
        "inpaint_full_res": True,
        "sampler_name": "DPM++ 2M Karras",  # Experiment with samplers
        "sampler_index": "Euler",
        "include_init_images": False,
        "send_images": True,
        "save_images": False,
        "face_restoration": ""
    })

    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=payload,
                                timeout=500)
    json_data = response.json()

    # Saving the JSON data to a file named 'data.json'
    with open('data.json', 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    # Extracting and saving the image
    image_data_base64 = json_data["images"][0]
    # Decode the Base64 image data
    image_data = base64.b64decode(image_data_base64)
    # Load the image using PIL
    image = Image.open(BytesIO(image_data))
    # Save the image
    image.save("output_image.png")


if __name__ == "__main__":
    # Define your URL and prompt here
    url = "https://collecting-americas-frank-falls.trycloudflare.com/"
    prompt = "Anime style, highly detailed"

    # Call the function to generate the image
    img2img(url=url, image_path="./output_image.png", prompt=prompt)
