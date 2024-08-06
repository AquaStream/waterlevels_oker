
# Installation and Contribution Guide

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

- Python 3.9 or higher
- Git

## Clone the Repository

First, clone the repository from GitHub to your local machine.

```bash
git clone https://github.com/AquaStream/waterlevels_oker.git
cd waterlevels_oker
```

## Setup the Environment

To set up the environment, execute the following commands:

```bash
chmod +x setup.sh
./setup.sh
```

The above commands will install Poetry, install the dependencies, activate the environment, and fetch the data in the `data/raw` folder.

## Contributing

We welcome contributions from the community. To contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with a proper commit structure.

### Commit Structure

Please follow this structure for your commit messages:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Example:

```
feat(weather): add new weather data fetching feature

This feature allows the application to fetch weather data from a new API source.

Signed-off-by: Your Name <your.email@example.com>
```

### Sign-off Commits

All commits must be signed off to indicate that you agree to the [Developer Certificate of Origin (DCO)](https://developercertificate.org/). You can sign off your commits by using the `-s` or `--signoff` option with your commit command:

```bash
git commit -s -m "your commit message"
```

## Building Documentation

To build the documentation and view the documentation on a local server using MkDocs:

```bash
mkdocs build && mkdocs serve
```


## Contact and Support

If you have any questions or need further assistance, please feel free to reach out to our team. You can also open an issue on our [GitHub repository](https://github.com/AquaStream/waterlevels_oker/issues).

---

We look forward to your contributions and feedback. Thank you for being a part of the Water Levels Oker project!
