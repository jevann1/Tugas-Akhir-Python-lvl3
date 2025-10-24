# Study Field Quiz

This project is a simple quiz application that helps users determine which field of study they might enjoy based on their preferences. The application features a user-friendly interface and presents a series of questions to the user, collecting their responses to provide insights into suitable study fields.

## Project Structure

```
study-field-quiz
├── src
│   ├── main.py               # Entry point of the application
│   ├── ui
│   │   ├── quiz_window.py     # Manages the quiz user interface
│   │   └── components.py       # Reusable UI components
│   ├── models
│   │   └── question.py         # Defines the Question class
│   ├── data
│   │   └── questions.json      # Contains quiz questions and answers
│   └── utils
│       └── scorer.py           # Functions for calculating scores
├── tests
│   └── test_quiz.py           # Unit tests for the application
├── requirements.txt           # Project dependencies
├── pyproject.toml             # Project configuration
└── README.md                  # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd study-field-quiz
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage

Upon running the application, users will be presented with a series of questions. Based on their answers, the application will suggest potential fields of study that align with their interests.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.