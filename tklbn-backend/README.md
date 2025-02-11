# TAKLUBAN: Filipino Native Language Profanity Detection

This project aims to detect profane language in Filipino native languages such as Tagalog, Bikol, and Cebuano using context-based methods instead of a profanity list.

## Getting Started

Follow these steps to set up the project on your local machine.

### Prerequisites

Ensure that the following software is installed on your system:

- Python 3.12
- Git
- VS Code (or any code editor of your choice)
- Java 22.0.2 or later

### Installation

1. **Clone the repository:**

   Open your terminal and run:

   ```bash
   git clone https://github.com/lalanglarano/TAKLUBAN-FILIPINO-NATIVE-LANGUAGE-PROFANE-DETECTION.git
   ```

2. **Navigate into the project directory:**

   ```bash
   cd TAKLUBAN-FILIPINO-NATIVE-LANGUAGE-PROFANE-DETECTION
   ```

3. **Create and activate a virtual environment:**

   Create a virtual environment to isolate project dependencies.

   - On Linux/Mac:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

4. **Install the required dependencies:**

   Install the Python libraries listed in `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

5. **Set up Java for the API:**

   Ensure Java 22.0.2 or a later version is installed to support Java-based modules used for the project. You can verify the installation by running:

   ```bash
   java -version
   ```

6. **Run the Flask application:**

   Once everything is set up, you can now run the Flask app.

   1. **Create a virtual environment**:

      Run the following command to create a virtual environment named `venv`:

      ```bash
      python -m venv venv
      ```

   2. **Activate the virtual environment** (if not already activated):
   
      - On Linux/Mac:
        ```bash
        source venv/bin/activate
        ```

      - On Windows:
        ```bash
        venv\Scripts\activate
        ```

   3. **Install the Python libraries listed in `requirements.txt` for venv:**
         ```bash
         pip install -r requirements.txt
         ```

   4. **Run the app:**
   
      ```bash
      python app.py
      ```

   This will start the Flask web server at `http://127.0.0.1:5000/`; you can use it to process sentences for profanity detection.
