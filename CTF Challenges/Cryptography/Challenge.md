# The Broken Cipher

## Mission

An intercepted communication was recovered from a compromised system.

The messages appear to be encrypted using a classical cipher. The attacker
made one mistake: the same short key was reused across multiple messages.

Your job is to analyze the ciphertext, recover the encryption key, decrypt
the messages, and uncover the hidden flag.

## Objective

- Identify the cipher being used.
- Recover the reused key.
- Decrypt the intercepted messages.
- Find the flag hidden inside the final message.

## Difficulty

Medium

## Points

250

## Tools

- CyberChef
- dCode
- Python
- Vigenère Cipher Decoder

## Start Here

1. Read all four intercepted messages carefully.
2. Look for repeated patterns and common words.
3. Determine what type of cipher could produce the ciphertext.
4. Investigate whether the same key is being reused.
5. Recover the key and decrypt the final message.

## Flag Format

`TECH{...}`

## Important

You do not need to attack the Cyber Arena server itself.

The provided evidence contains everything required to solve the challenge.