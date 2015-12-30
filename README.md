# FB-message-grapher
A python utility for outputting various statistics about the facebook messages you send. By reading the messages.htm file provided
by Facebook, we retrieve all messages sent by your profile, and are able to run analytical algorithms on it.

Features include:
  - Reads entire Facebook message history

## Install Instructions
To run this program requires 2 dependencies.
  - The latest version of python3
  - The python-dateutil package (install using "pip" or the typical methods for your operating system)

## Running
  1. Navigate to your Facebook homepage, and click the menu in the top right corner. (Triangle shaped button)
  2. Click settings
  3. On this page you will find a blue link named "Download a copy" of your facebook data. Click this and go through the process to download
  4. Run `python3 analyse-message <path-to-file>`

## Instructions
After the analyser completes the parsing of all your messages, "Ready!" will be displayed, as well as a prompt
for entering commands. This is called the command prompt.

### Pulling up Documentation
  `help "<command(optional)>"`

  To show documentation for the commands avaliable run "help"
  
  It is also possible to show documentation for only a specific command by providing it as an argument e.g `help "help"`

### Storing results to a variable
  `<command-and-arguments> to <variable>`

  The command prompt also allows the storing of calculation results to a variable.
  (Support for multiple variables is not yet supported)

  The variable is automatically declared, or overwritten when stored to.

  To use this feature simply use the `to` directive. e.g `help to helpString`
