import redis
from redis_lru import RedisLRU

import connect
from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag):
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author):
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def parse(user_input):

    split_text = user_input.split(':')
    command = split_text[0].lower().strip()

    if len(split_text) > 1:
        args = split_text[1].lower().strip().split(',')
    else:
        args = None
    return command, args


def main():
    while True:

        user_input = input('Enter command: ')
        command, args = parse(user_input)

        match command:
            case 'exit':
                print("The script has completed its work.")
                break
            case 'name':
                print(find_by_author(*args))
            case 'tag':
                print(find_by_tag(*args))
            case 'tags':
                for tag in args:
                    print(find_by_tag(tag))
            case _:
                print("Unknown command.")


if __name__ == '__main__':
    main()
