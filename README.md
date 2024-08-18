# Chemical Information and Comparison Tool

This project is a web-based tool that allows users to search for chemical compounds, retrieve detailed information about
them, and visually compare their molecular structures using a 3D ball-and-stick model.

## Features

- **Search Compounds**: Users can search for chemical compounds by name.
- **Compound Information**: Detailed information about each compound is displayed, including the CID, molecular formula,
  molecular weight, and IUPAC name.
- **3D Molecular Visualization**: Compounds are rendered as interactive 3D models using a ball-and-stick style, which
  users can explore directly in the browser.
- **Structural Similarity**: When comparing two compounds, the tool calculates and displays their structural similarity
  using the Tanimoto coefficient.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **3D Visualization**: [3Dmol.js](https://3dmol.csb.pitt.edu/) is used for rendering the 3D molecular models.
- **Backend**: Flask (Python) to handle requests and fetch compound data from PubChem using the `pubchempy` library.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/lucas-svi/cheminfoapp.git
   cd cheminfoapp
2. Install Python dependencies:
   ```bash
   pip install flask pubchempy
3. Run the Flask server:
   ```bash
   python main.py

# Usage

## Searching for Compounds

1. Enter the name of a chemical compound in the search field.
2. The application will fetch and display a list of possible matches.
3. Select a compound to load its detailed information.

## Comparing Compounds

1. Enter the names of two chemical compounds in the provided fields.
2. Click the "Fetch and Compare" button.
3. The application will display detailed information for both compounds, render their 3D models, and calculate their
   structural similarity.

## Interacting with 3D Models

* Click on the compound image to load its 3D model.
* The model will be displayed in an overlay. Use your mouse to rotate, zoom, and explore the molecular structure.

# Customization

## Ball-and-Stick Model

You can customize the appearance of the ball-and-stick models by adjusting the following parameters in the loadMolecule
function:

* **Atom Size (Sphere Scale)**: You can use the slider at the bottom of the model to change the size of the atoms.
* **Bond Thickness (Stick Radius)**: You can use the slider at the bottom of the model to change the thickness of the bonds.