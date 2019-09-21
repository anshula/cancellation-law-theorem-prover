import os
import re
import pexpect
import time

from errors import *

class CoqInterface:
    """
    Python to Coqtop interface, using pexpect.

    Referenced in: https://github.com/ml4tp/gamepad/blob/master/gamepad/pycoqtop/coqtop.py
    Taken from: https://github.com/cpitclaudel/coq-rst/blob/master/utils/python/coqrst/repl/coqtop.py
    """

    COQTOP_PROMPT = re.compile("\r\n[^< ]+ < ")

    def __init__(self, env, coqtop_bin=None, color=False, args=None):
        """
        Configure a coqtop instance (but don't start it yet).
        
        coqtop_bin
            The path to coqtop; uses $COQBIN by default, falling back to "coqtop"
        color
            When True, tell coqtop to produce ANSI color codes (see the ansicolors module)
        args
            Additional arugments to coqtop.
        """
        self.env = env

        # compile necessary coq code
        os.system("coqc coq/group.v")
        
        # self.coqtop_bin = coqtop_bin or os.getenv('COQBIN') or "coqtop"
        self.coqtop_bin = "coqtop"
        self.args = (args or []) + ["-color", "on"] * color
        self.coqtop = None

        if self.coqtop:
            raise ValueError("This module isn't re-entrant")
        self.coqtop = pexpect.spawn(self.coqtop_bin, args=self.args, echo=False, encoding="utf-8")
        # Disable delays (http://pexpect.readthedocs.io/en/stable/commonissues.html?highlight=delaybeforesend)
        self.coqtop.delaybeforesend = 0
        self.next_prompt()

    
    def exit(self):
        self.coqtop.kill(9)

    def next_prompt(self):
        "Wait for the next coqtop prompt, and return the output preceeding it."
        self.coqtop.expect(CoqInterface.COQTOP_PROMPT, timeout = 1)
        return self.coqtop.before

    def sendone(self, sentence):
        """Send a single sentence to coqtop.
        :sentence: One Coq sentence (otherwise, Coqtop will produce multiple
                   prompts and we'll get confused)
        """
        # Don't undo if it's going to undo setting up the theorem goals
        if ("Undo" in sentence) and (len(self.env.state.past_actions) <= 4):
            raise UndoError

        # Suppress newlines, but not spaces: they are significant in notations
        sentence = re.sub(r"[\r\n]+", " ", sentence).strip()
        self.coqtop.sendline(sentence)
        response = self.next_prompt()

        # Determine if there are errors
        if "Error" in response and (response.count("Error") > response.count("No such assumption")):
            # undo all of the successful actions
            num_successful_actions = sentence.count(".") - response.count("Error")
            for _ in range(num_successful_actions): self.sendone("Undo.")

            # raise an error so we don't add it to list of past actions or change environment state
            raise CoqError

        return response