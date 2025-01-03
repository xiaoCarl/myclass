import os
import config
from deepseek_api import DeepSeekClient

class ChatApp:
    def __init__(self):
        self.client = DeepSeekClient(config.API_KEY)
        
    def run(self):
        print("DeepSeek Chat - 输入'退出'结束对话")
        while True:
            user_input = input("你: ")
            if user_input.lower() in ['退出', 'exit']:
                break
                
            print("AI: ", end="", flush=True)
            for chunk in self.client.chat(user_input):
                print(chunk, end="", flush=True)
            print()

if __name__ == "__main__":
    app = ChatApp()
    app.run()
