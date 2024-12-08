# MyBassTranscriber 🎸

This project is born out of the necessity to simplify learning bass guitar lines and solos. I like to play and learn new tecniques by listening to songs but most of the times, even though I have a good hear, either the bass-line is not easy or is hard to get.  
I (still) don't know how to read music scripts, hence I often find myself searching for tabs and looking at YouTube videos.. but sometimes is not good enough.  

I want a way to get tabs out of songs and don't want to pay for it. So.. here it is.
This project is more like an opportunity to learn new stuff and play with ML and AI, but hopefully I'll get to something that can actually fullfil my goal. 
Maybe this can be helpful for you as well.. or maybe not.

It doesn't matter. You can use this code as you like or simply ignore it. 

I'd **really** appreciate feedbacks and contribution though 😃

## Run Flask webserver

As of the moment, the app run on a flask webserver to provide a simple interface to test the features.

Run flask from project root
```
$ python src/app.py
```

## Testing and packaging
The project is tested over multiple environments using [tox](https://tox.wiki/en/4.23.2/):

Run tox from project root
```
$ tox
```

## Linting
The project uses [ruff](https://docs.astral.sh/) for linting and code formatting.

Run ruff from project root:
```
$ ruff check   # Lint all files in the current directory.
$ ruff check --fix  # Lint all files in the current directory and fix errors.
$ ruff format  # Format all files in the current directory.
```