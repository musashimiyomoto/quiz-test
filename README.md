It is necessary to make a simple service for testing on any topic.
Those. there are multiple choice tests, one or more options must be correct.
Tests are grouped into test sets, which the user can then run and see their result.

# Functional parts of the service:
### 1) User registration.
### 2) User authentication.
### 3) Registered users can:
* Pass any of the test suites.
* Each question has its own unique URL and includes the question ID in the GET parameter.
* After submitting an answer to a question, the next question should be opened using the GET method.
* It is impossible to jump over questions, leave a question unanswered, return to already answered questions.
* If the user closed the question page, then when returning to the same test set, he should get to the question that he left off earlier.
### 4) After testing is completed, show the result:
* Number of correct/incorrect answers.
* Percentage of correct answers.
### 5) Admin panel. Standard Django admin.
* Standard user section.
* Section with test sets.
* Validation that among the answer options there must be at least 1 correct option.
* Validation that all options cannot be correct.
