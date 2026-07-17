from dotenv import load_dotenv
import os

# carregar variáveis de ambiente
load_dotenv()

from app import SpeechAIApp


def main():
    env = os.getenv("PROJECT_ENV", "undefined")
    print("[ENV]", env)

    app = SpeechAIApp()
    app.run()


if __name__ == "__main__":
    main()
