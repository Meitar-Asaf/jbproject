import re


def is_valid_email(email):
    pattern = re.compile(
        "^[\\w]+.{0,1}[\\w.+1-9]*@[\\w-]+([\\w1-9]*\\.[\\w1-9]+)*\\.[\\w]{3}$")
    print(re.fullmatch(pattern, email) is not None)


is_valid_email("invalid..email@example.com")
