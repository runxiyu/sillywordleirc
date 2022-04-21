#!/usr/bin/python3
from random import choice
import sys
import miniirc

allowed_solutions = [
    w.strip().upper() for w in open("solutions.txt", "r").readlines()
]
allowed_guesses = set(
    [w.strip().upper() for w in open("guesses.txt", "r").readlines()]
)
allowed_guesses = allowed_guesses | set(allowed_solutions)

ALLOWED_GUESSES = 6

ext = lambda s: "\x0303" + s + "\x0f"
ptl = lambda s: "\x0307" + s + "\x0f"
wrg = lambda s: "\x0f" + s + "\x0f"


def check_guess(guess, answer):
    res = []
    for i, letter in enumerate(guess):
        if answer[i] == guess[i]:
            res += ext(letter)
        elif letter in answer:
            res += ptl(letter)
        else:
            res += wrg(letter)
    return "".join(res)


nick = "WordGuess"
ident = nick
realname = "git://git.andrewyu.org/wordle.git"
identity = None
debug = True
channels = ["#LibreIRC", "#LibreSpeech"]
prefix = "%"

ip = "irc.andrewyu.org"
port = 6697

irc = miniirc.IRC(
    ip,
    port,
    nick,
    channels,
    ident=ident,
    realname=realname,
    ns_identity=identity,
    debug=debug,
    auto_connect=False,
)

state = {}

@irc.Handler("PRIVMSG", colon=False)
def handle_privmsg(irc, hostmask, args):
    channel = args[0]
    text = args[-1].split(" ")
    cmd = text[0].lower()
    sendto = channel if channel.startswith("#") else hostmask[0]
    if cmd.startswith(prefix):
        cmd = cmd[len(prefix) :]
        if cmd == "start":
            state[hostmask[0]] = {"guessed": [], "accumulation": []}
            state[hostmask[0]]["solution"] = choice(allowed_solutions)
            print(state[hostmask[0]]["solution"])
            irc.msg(sendto, hostmask[0] + ": You have started a game.  Your word has " + str(len(state[hostmask[0]]["solution"])) + " letters.  You have " + str(ALLOWED_GUESSES) + " attempts.  Use " + prefix + "guess to guess.")
        elif cmd == "guess":
            if hostmask[0] not in state.keys():
                irc.msg(sendto, hostmask[0] + ": You aren't in a game.  Use " + prefix + "start to use.")
            guess = " ".join(text[1:]).strip().upper()
            if guess in state[hostmask[0]]["guessed"]:
                irc.msg(sendto, hostmask[0] + ": %s has already been guessed." % guess)
                return
            elif guess not in allowed_guesses:
                irc.msg(sendto, hostmask[0] + ": %s isn't in my dictionary." % guess)
                return
            state[hostmask[0]]["guessed"].append(guess)
            res = check_guess(guess, state[hostmask[0]]["solution"])
            state[hostmask[0]]["accumulation"].append(res)
            irc.msg(sendto, hostmask[0] + ": " + str(' '.join(state[hostmask[0]]["accumulation"])))
            if guess == state[hostmask[0]]["solution"]:
                irc.msg(seneto, hostmask[0] + ": %s is indeed the solution." % guess)
                del state[hostmask[0]]
                return
            elif len(state[hostmask[0]]["accumulation"]) >= ALLOWED_GUESSES:
                irc.msg(sendto, hostmask[0] + ": You used up your chances!  It was %s." % state[hostmask[0]]["solution"])
                del state[hostmask[0]]
                return 


if __name__ == "__main__":
    irc.connect()
