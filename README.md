# learn_python_grading_journal
School digital grading book service backend created for learning purposes.


# API

```
# Return all educational groups.
GET /groups/

# Return all subjects within group.
GET /groups/1/subjects/

# Return all pupils within group.
GET /groups/1/pupils/

# All pupil's grades for specific subject within group.
GET /groups/1/subjects/1/grades/

# Set grade for specific pupil and subject.
POST /pupils/1/subjects/1/grades/
{"value": 5}
```


