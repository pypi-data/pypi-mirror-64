import typing as ty
import re


RP = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def markdown_string_link_generator(markdown_string: str) -> ty.Generator:
    for link in RP.finditer(markdown_string):
        yield type(
            "link", (), {"word": link.groups()[0], "entity": link.groups()[1], "start": link.start(0), "end": link.end(0)})


def markdown_links2entity_list(markdown_string: str) -> ty.Tuple:
    linkless_string = ""
    entities = []
    idx = 0
    for link in markdown_string_link_generator(markdown_string):
        linkless_string += markdown_string[idx:link.start]
        word_idx = len(linkless_string)
        linkless_string += link.word
        idx = link.end
        entities.append((word_idx, word_idx + len(link.word), link.entity))  # Append to entities

    linkless_string += markdown_string[link.end:]  # Add the rest of the string
    return (linkless_string, {"entities": entities})


def entity_list2markdown_links(text: str, entities: ty.List) -> str:
    markdown_string = ""
    idx = 0
    for start, end, entity in entities:
        markdown_string += text[idx:start] + f"[{text[start:end]}]({entity})"
        idx = end
    markdown_string += text[idx:]
    return markdown_string
