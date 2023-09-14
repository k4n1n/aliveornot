# aliveornot

Aliveornot is a simple GUI tool that helps monitor the availability of various domains or hosts. Each host is represented by a colored square:
- **Green**: The host is alive and responding.
- **Red**: The host is not responding.
- **Black**: The hostname could not be resolved.

## Installation

1. Ensure you have Python (version 3.x) installed. You can download it from [python.org](https://www.python.org/downloads/).

2. Clone or download this repository to your local machine.

3. Navigate to the directory containing the `aliveornot.py` and the required libraries using your terminal or command prompt.

4. Install the required libraries:

```
tkinter
ping3
```

## Usage

1. To start the application, run the following command:

```
python aliveornot.py
```

2. The GUI window will open. Use the "Add Host" button to add new hosts/domains to the list.

3. Every two minutes, the application will automatically check the status of each host/domain and update the color of the corresponding square.

4. To manually check the status of all hosts/domains, click the "Ping Now" button.

5. To remove a host/domain from the list, select it and click the "Remove Host" button.

## Note

For certain hosts, especially `localhost`, you might need elevated permissions to determine their status. Ensure you have the necessary permissions to execute socket connections for the domains you're monitoring.
