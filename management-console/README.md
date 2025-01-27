# Management Console Installer

This project provides an installer for the Management Console application, which is designed for managing and monitoring systems through a user-friendly interface.

## Project Structure

- **src/**: Contains the main application code and resources.
  - **SP_Management_Console.py**: The main application code, including classes for login, monitoring, and the admin panel.
  - **requirements.txt**: Lists the dependencies required for the project.
  - **setup.py**: The setup script for packaging the application.
  - **resources/**: Contains application resources.
    - **app.desktop**: Desktop entry file for launching the application.
    - **app.ico**: Icon file for the application.

- **README.md**: Documentation for the project, including installation instructions and usage.

- **.env**: Contains environment variables used by the application.

## Installation Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd management-console-installer
   ```

2. Navigate to the `src` directory:
   ```
   cd src
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the setup script to create the installer:
   ```
   python setup.py install
   ```

## Usage

After installation, you can launch the Management Console application from your desktop environment or by executing the following command in your terminal:
```
python SP_Management_Console.py
```

## Environment Variables

Make sure to configure the `.env` file with the necessary environment variables, such as database credentials and other configuration settings, before running the application.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.