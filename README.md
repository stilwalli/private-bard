# My Awesome Project

This is a brief description of my awesome project.

![Project Screenshot](images/bard.png)

## Features

* Feature 1
* Feature 2
* Feature 3

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for   
 development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.


curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" \
  -d '{"user_prompt": "Give me sample letter for resignation in 20 words"}' \
  "https://private-bard-906035941682.us-central1.run.app/callPrivateGemini"



