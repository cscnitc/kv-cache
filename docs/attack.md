# Attack

For now, fill in the two files in the `attack/` folder.

`victim_prompt.py` should have the fake planted content we'll attack while testing, some small string with sensitive info like company name or internal instruction.

`candidates.py` should have the initial guessing wordlist. A fixed list of plausible values for the known template value. We're not starting from scratch with an open-ended search in the beginning.