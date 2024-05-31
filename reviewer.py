import openai
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

if "OPENAI_API_KEY" not in os.environ:
  raise ValueError("OPENAI_API_KEY is missing from the .env file, please provide one.")
openai.api_key = os.environ.get("OPENAI_API_KEY")

PROMPT = """
You will receive a file's contents as text. Genearate a code review for the ifle.
Indicate what changes should be made to improve its style, performance,
readibility, and maintainability. If there are any reputable libraries that
could be introduced to improve the code, suggest them. Be kind and constructive.
For each suggested chante, include line numbers to which you are referring.
"""

def code_review(file_path, model):
  with open(file_path, "r") as file:
    file_content = file.read()
    generated_code_review = make_code_review_request(file_content, model)
    print(generated_code_review)


def make_code_review_request(file_content, model):
  messages = [
    {
      "role": "system",
      "content": f"{PROMPT}"
    }
  ]
  messages.append({
    "role": "user",
    "content": file_content
  })
  response = openai.chat.completions.create(
    model=model,
    messages=messages
  )
  return response.choices[0].message.content

def main():
  parser = argparse.ArgumentParser(description="Simple code reviewer for a file")

  parser.add_argument("file", type=str, help="A relative or absolute path to the file to be reviewed")
  parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="The model to use for the code review")
  args = parser.parse_args()

  code_review(args.file, args.model)

if __name__ == "__main__":
  main()