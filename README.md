
# Cartesi Python Student Registration and Course Management

This project demonstrates how to use Cartesi Rollups to create a student registration and course management system using Python. Students can register with their email, add courses with grades, and query their results using their email. All data is persisted in a CSV file.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Cartesi Rollup Server](#cartesi-rollup-server)

## Requirements

- Python 3.11+
- `requests` library

## Setup

 **Clone the repository:**

```sh
git clone repo_url
cd repo_dir
```

## Usage

### Register a Student

To register a student, send a payload with the format `register|email@example.com` to the Rollup server.

### Add Course and Grade

To add a course and grade for a registered student, send a payload with the format `add_course|email@example.com|CourseName:A` to the Rollup server.

### Query Student Results

To query a student's results, send a payload with the student's email to the Rollup server.

## Code Explanation

### Main Functions

- **load_students**: Loads student data from a CSV file into a dictionary.
- **save_students**: Saves the student data to a CSV file.
- **handle_advance**: Processes registration and course addition requests.
- **handle_inspect**: Processes requests to inspect a student's data.

### CSV File Handling

- The CSV file `students.csv` stores each student's email and their courses with grades as a JSON string.

### Example CSV Entry

```csv
email@example.com,"{\"CourseName\": \"A\"}"
```

## Conclusion

This project demonstrates how to use Cartesi Rollups to manage student registration and courses using Python. The data is persisted in a CSV file, making it easy to manage and query student information. For more information on Cartesi Rollups, refer to the [official documentation](https://cartesi.io/docs/).