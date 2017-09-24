# About
This is an n-gram viewer for a small dataset of books from 2012-2016

# Installation
1. Download and unzip (or clone) the git repository.
2. Open a terminal and navigate to the folder where you extracted the repository. For example `cd ~/Downloads/NgramViewer-master/`.
3. Install dependencies.
    1. Make sure the installation script is executable with `chmod +x ./install.sh`
    2. Run `./install.sh`. This may take a while.

# Usage
1. Make sure the execution script is executable with `chmod +x ./test/ngram_viewer.sh`.
2. You can run the application with `./test/ngram_viewer.sh`. Initialization can take a few seconds.

The execution script will start a Bokeh server instance and automatically open a browser window. It currently supports spelling suggestions and can generate synonym suggestions. While spelling suggestions are very fast, generating synonyms can be an extremely slow process and is therefore not performed by default on each query. In order to generate synonyms, you need to click the 'Generate synonyms' button. This will populate the drop-down menu with potential word replacements.
