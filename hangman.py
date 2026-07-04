import random

words = [
    "python",
    "computer",
    "developer",
    "programming",
    "internship",
    "keyboard",
    "internet",
    "software",
    "algorithm",
    "database"
]

secret_word = random.choice(words)
guessed_letters = []
attempts = 6

print("=" * 50)
print("        CODEALPHA HANGMAN GAME")
print("=" * 50)
print("Guess the word one letter at a time.")
print("You have", attempts, "lives.\n")

while attempts > 0:

    display_word = ""

    for letter in secret_word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "

    print(display_word)

    if "_" not in display_word:
        print("\n🎉 Congratulations! You guessed the word:", secret_word)
        break

    guess = input("\nEnter a letter: ").lower()

    if len(guess) != 1 or not guess.isalpha():
        print("Please enter only one alphabet letter.\n")
        continue

    if guess in guessed_letters:
        print("You already guessed that letter.\n")
        continue

    guessed_letters.append(guess)

    if guess not in secret_word:
        attempts -= 1
        print("❌ Wrong guess!")
        print("Remaining lives:", attempts, "\n")

if attempts == 0:
    print("\n💀 Game Over!")
    print("The correct word was:", secret_word)