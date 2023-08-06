# Nyckelmästaren
  
(this means Keymaster in Swedish.)

A text-based action-RPG game. Developed by Adam Winograd and I.

Inspired by games like Zork, A Link To The Past, Dragon Warrior and Mother.

![Game Poster](https://i.imgur.com/XUv2UnH.png)

## Dependencies:
- Simpleaudio: https://github.com/hamiltron/py-simple-audio
- Viu: https://github.com/atanunq/viu
- Pillow: https://github.com/python-pillow/Pillow
- An installation of Rust: https://www.rust-lang.org/learn/get-started

All in-game graphics were made without any external libraries, which I'm really happy about. It looks like an Atari 2600 game!

## Commands:
- w / north / go north
- d / east / go east
- s / south / go south
- a / west / go west
- words of encouragement
- use / item
- inventory
- location
- settings / options
- help

## Before running the game, run these commands in your terminal:
- curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
- cargo install viu