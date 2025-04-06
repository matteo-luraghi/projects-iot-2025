import argparse

from q1 import answer_q1
from q2 import answer_q2
from q3 import answer_q3
from q4 import answer_q4
from q5 import answer_q5
from q6 import answer_q6
from q7 import answer_q7


def main():
    parser = argparse.ArgumentParser(
        description="Call the corresponding answer function based on the argument passed."
    )
    parser.add_argument(
        "question_number",
        type=int,
        help="The number of the question (e.g., -1, -2, etc.)",
    )

    # Parse the command-line argument
    args = parser.parse_args()

    # Map the argument to the corresponding function
    question_map = {
        -1: answer_q1,
        -2: answer_q2,
        -3: answer_q3,
        -4: answer_q4,
        -5: answer_q5,
        -6: answer_q6,
        -7: answer_q7,
    }

    # Call the corresponding function based on the input
    if args.question_number in question_map:
        question_map[args.question_number]()
    else:
        print("Invalid question number!")


if __name__ == "__main__":
    main()
