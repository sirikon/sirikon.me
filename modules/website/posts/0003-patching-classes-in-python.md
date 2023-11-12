---
title: Patching classes in Python
---

Oh, so you found yourself needing to patch a class in Python? _again_? And some
neckbeard is telling you on the internet you shouldn't do it?

I'm about to give you a loaded gun buddy.

```python
class Animal:
    def announce(self):
        print("I'm " + self.__class__.__name__)


class Goose(Animal):
    def honk(self, name: str):
        super().announce()
        print(f"HONK. HEY {name.upper()}. GET OFF MY LAWN.")

    def do_your_thing(self):
        self.honk("Stranger")


class AmericanGoose(Goose):
    def honk(self, name: str):
        super().honk(name)
        print("BANG. BANG.")


g = AmericanGoose()
g.do_your_thing()
```

```
I'm AmericanGoose
HONK. HEY STRANGER. GET OFF MY LAWN.
BANG. BANG.
```

Let's say you want to make geese more polite.

```python
def make_geese_polite():
    # pick the old method if you need it.
    old_honk = Goose.honk

    # define __class__ pointing to the class to patch, so calls
    # to super() work.
    __class__ = Goose

    def new_honk(self, name: str):
        print("-- Polite Goose")
        super().announce()
        print(f"Good evening {name}. May you please get off my lawn.")
        print("-- Original Goose")
        # call the old method by passing `self`
        old_honk(self, name)
        print("-- End")

    Goose.honk = new_honk


make_geese_polite()
g.do_your_thing()
```

```
-- Polite Goose
I'm AmericanGoose
Good evening Stranger. May you please get off my lawn.
-- Original Goose
I'm AmericanGoose
HONK. HEY STRANGER. GET OFF MY LAWN.
-- End
BANG. BANG.
```

Use this power wisely.

EDIT: Replacing "gooses" with "geese" because I'm an uneducated fuck.

*[neckbeard]: Demonym for StackOverflow and subreddits about programming