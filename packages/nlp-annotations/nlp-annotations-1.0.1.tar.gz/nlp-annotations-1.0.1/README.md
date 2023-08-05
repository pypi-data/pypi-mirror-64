# NLP Annotations

A simple python package for dealing with different nlp annotation styles.
No dependencies, and is very fast due to only using regular expressions.

You can install it with:

```bash
pip3 install nlp-annotations
```

## Annotation Types

The following are the annotation types we support and how to convert it to
another type.

### Markdown Links

(Used by Rasa, etc...), these are in the form:

```markdown
The weather is [sunny](weather) and the sky is [blue](color).
```

To convert this to an _entity list_ you can:

```python
from nlp_annotations import markdown_links2entity_list
markdown_links2entity_list("The weather is [sunny](weather) and the sky is [blue](color).")
# ('The weather is sunny and the sky is blue.', {'entities': [(15, 20, 'weather'), (36, 40, 'color')]})
```

For other situations that you may wish to add extra logic, there is also a generator:

```python
from nlp_annotations import markdown_string_link_generator

for link in markdown_string_link_generator("The weather is [sunny](weather) and the sky is [blue](color)."):
    print(f"- word={link.word}, entity={link.entity}, start={link.start}, end={link.end}")

# - word=sunny, entity=weather, start=15, end=31
# - word=blue, entity=color, start=47, end=60
```

### Entity List

(Used by Spacy, etc...), these are in the form:

```python
('The weather is sunny and the sky is blue.', {'entities': [(15, 20, 'weather'), (36, 40, 'color')]})
```

To convert this to a _markdown links_ string, you can:

```python
from nlp_annotations import entity_list2markdown_links
entity_list2markdown_links("The weather is sunny and the sky is blue.", [(15, 20, 'weather'), (36, 40, 'color')])
# 'The weather is [sunny](weather) and the sky is [blue](color).'
```
