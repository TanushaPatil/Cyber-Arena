# The Final Puzzle

## Scenario

A mysterious challenge server has appeared inside Cyber Arena.

The server generates a sequence of mathematical questions and
expects the correct answers within a strict time limit.

Solving the questions manually is too slow.

Your task is to connect to the service, understand its protocol,
automate the calculations and recover the final encoded message.

## Objective

1. Connect to the challenge server.
2. Observe the question format.
3. Solve the generated mathematical questions.
4. Submit all answers within the time limit.
5. Capture the final encoded value.
6. Decode the value repeatedly until the flag is revealed.

## Challenge Service

Host:

    127.0.0.1

Port:

    5002

## Recommended Tools

- Python
- Socket programming
- pwntools
- Terminal / Netcat

## Suggested Approach

Create a Python script that:

1. Connects to the server.
2. Reads each question.
3. Extracts the numbers and operator.
4. Calculates the answer.
5. Sends the answer back.
6. Continues until all questions are solved.
7. Saves the final encoded response.

## Important

The final response is encoded.

Do not immediately assume that the first decoded value
is the final answer.

## Flag

Submit the recovered flag through Cyber Arena.