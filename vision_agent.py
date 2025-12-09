from groq import Groq
import base64
from dotenv import load_dotenv
import os

load_dotenv()


class VisionAgent:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.environ["GROQ_KEY"])


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


    @staticmethod
    def read_image(image_path):
      with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


    
    def ask_vison_model(self, user_interaction, image_path):

        response = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": VisionAgent.read_file("./context.txt")
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": user_interaction},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{VisionAgent.read_image(image_path)}",
                            },
                        },
                    ],
                }
            ],
            model="meta-llama/llama-4-scout-17b-16e-instruct",
        ).choices[0].message.content


        return response


if __name__ == "__main__":
    vision_agent = VisionAgent()
    response = vision_agent.ask_vison_model(
                                user_interaction="Ce monsieur t'as balancé aux flics, est ce que tu le reconnais ?",\
                                image_path="./images/image_1.jpeg"
                                )

    print(response)