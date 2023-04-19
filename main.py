import logging
import datetime
import random
from string import ascii_letters
import openai
import dotenv

name = __name__
_log = logging.getLogger(name)
_log.setLevel(logging.DEBUG)

_log_handler = logging.FileHandler(filename=f'{name}.log',
                                   encoding='utf-8',
                                   mode="a")
_log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
_log_handler.setFormatter(_log_formatter)

_log.addHandler(_log_handler)

openai.api_key = dotenv.get_key(dotenv_path='.env', key_to_get='OPENAI_API_KEY')
model_engine: str = dotenv.get_key(dotenv_path='.env', key_to_get='MODEL_ENGINE')
max_tokens: int = int(dotenv.get_key(dotenv_path='.env', key_to_get='MAX_TOKENS'))

max_prompts = 5

prompt = [
    {"role": "system", "content": "You’re a kind helpful assistant"}
]


def _get_now_time():
    return datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")


def _text_tag(text: str):
    return f"\033[36m{text}\033[0m"


def _gen_random_string(size: int):
    string_ = ''
    for _ in range(size):
        string_ += random.choice(ascii_letters)
    return string_


def _prompt_correction():
    if len(prompt) == max_prompts:
        del prompt[1]
        del prompt[2]


def _save_dialog(_dialog: list[str]):
    filename_ = f'{_get_now_time()}_dialog'
    format_ = '.txt'
    path_ = 'dialogs/'

    with open(path_ + filename_ + format_, 'w', encoding='utf-8') as file:
        file.write("\n".join(_dialog))

    _log.info(f'FILE CREATED {filename_ + format_}')


if __name__ == '__main__':
    _log.info("START")
    dialog_ = []

    try:
        while True:
            content = input("User: ")

            prompt.append({"role": "user", "content": content})

            dialog_.append(f'User: {content}')

            completion = openai.ChatCompletion.create(
                model=model_engine,
                max_tokens=max_tokens,
                messages=prompt
            )

            _log.info(f"GET COMPLETION {completion}")

            chat_response = completion.choices[0].message.content
            print(f'{_text_tag("ChatGPT")}: {chat_response}')
            prompt.append({"role": "assistant", "content": chat_response})
            dialog_.append(f'ChatGPT: {chat_response}')

            _prompt_correction()
    except KeyboardInterrupt:
        _save_dialog(_dialog=dialog_)
        exit()

# def _translater(content_):
#     prompt_for_translate = [{"role": "system", "content": "You translate russian language to english ."},
#                             {"role": "user", "content": content_}]
#     completion_ = openai.ChatCompletion.create(
#         model=model_engine,
#         max_tokens=max_tokens,
#         messages=prompt_for_translate
#     )
#     return completion_.choices[0].message.content
# task = "Облако ядерного взрыва, картина маслом"
# prompt_for_dall = _translater(task)
# print(f'{_get_now_time()} Prompt done "{prompt_for_dall}"')
#
# response = openai.Image.create(prompt=prompt_for_dall, n=1, size="1024x1024")
# image_url = response['data'][0]['url']
# print(f'{_get_now_time()} Url done "{image_url}"')
#
# image = Image.open(urlopen(image_url))
# print(f'{_get_now_time()} Image done')
# image.show()

# image.save(f'{_gen_random_string(7)}.png')
