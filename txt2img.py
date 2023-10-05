import json
import base64
import requests
from PIL import Image
from io import BytesIO

headers = {'accept': 'application/json', 'Content-Type': 'application/json'}


def txt2img(url,
            prompt="Beautiful Landscape, Highly Detailed, HD",
            steps=30,
            cfg_scale=7.5,
            width=640,
            height=832,
            seed=-1):
    url = f"{url}sdapi/v1/txt2img"
    prompt = prompt

    payload = json.dumps({
        "enable_hr": False,
        "denoising_strength": 0.543234,
        "firstphase_width": 621.342,
        "firstphase_height": 894.234,
        "hr_scale": 1.98765,
        "hr_upscaler": "lanczos",
        "hr_second_pass_steps": 56,
        "hr_resize_x": 987.654,
        "hr_resize_y": 234.567,
        "hr_sampler_name": "Euler",
        "hr_prompt": "",
        "hr_negative_prompt": "",
        "prompt": prompt,
        "styles": ["photorealistic", "cartoonish", "abstract"],
        "seed": seed,
        "subseed": -1,
        "subseed_strength": 0.23456,
        "seed_resize_from_h": 567.89,
        "seed_resize_from_w": 987.65,
        "sampler_name": "DPM++ 2M Karras",
        "batch_size": 1,
        "n_iter": 1,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "width": width,
        "height": height,
        "restore_faces": True,
        "tiling": False,
        "do_not_save_samples": True,
        "do_not_save_grid": False,
        "negative_prompt":
        "Watermark, Text, deformed, bad anatomy, disfigured, poorly drawn face, mutated, extra limb, ugly, poorly drawn hands, missing limb, floating limbs, disconnected limbs, disconnected head, malformed hands, long neck, mutated hands and fingers, bad hands, missing fingers, cropped, worst quality, low quality, mutation, poorly drawn, huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, disappearing calf, disappearing legs, missing fingers, fused fingers, abnormal eye proportion, Abnormal hands, abnormal legs, abnormal feet,  abnormal fingers",
        "eta": 0.78945,
        "s_min_uncond": 0.34567,
        "s_churn": 0.12345,
        "s_tmax": 0.98765,
        "s_tmin": 0.23456,
        "s_noise": 0.65432,
        "override_settings": {},
        "override_settings_restore_afterwards": True,
        "script_args": [],
        "sampler_index": "Euler",
        "script_name": "",
        "send_images": True,
        "save_images": False,
        "alwayson_scripts": {},
        "face_restoration": "CodeFormer"
    })
    response = requests.request("POST",
                                url,
                                headers=headers,
                                data=payload,
                                timeout=500)
    json_data = response.json()
    # print(json_data)

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
    url = "https://collecting-americas-frank-falls.trycloudflare.com/"
    prompt = "beautiful women, anime, HQ"
    txt2img(url=url, prompt=prompt, steps=50)
