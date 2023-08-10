# Character Ranking Cards Generator

This project generates character ranking cards based on input rankings and character images. Each card showcases two characters, their combined ranking, and additional visual elements for aesthetics.

## Overview

The project reads the rankings from a file named `ranking.txt`, fetches character images from the `renders` folder, and compiles them into visually appealing cards. Additionally, it creates a composite image showcasing the top 8 rankings.

## Features

- **Dynamic Resizing**: Character images are dynamically resized to fit the card dimensions.
- **Visual Effects**: Each card includes gradient backgrounds, rounded edges, and other visual elements to enhance appearance.
- **Text Effects**: Winner names and rankings on the cards have dynamic font resizing, outlines, and drop shadows for better visibility and aesthetics.
- **Composite Image**: The top 8 rankings are compiled into one image for an overall view.

## How to Use

1. Ensure you have Python and the required libraries installed.
2. Place character images in the `renders` folder. The project currently supports `.png` images.
3. Update the `ranking.txt` file with the desired rankings. The format is `Winner Name, Character1, Character2`.
4. Run `main.py` to generate the ranking cards and the composite image.
5. Check the `rankings` folder for the generated images.

## Customizations

- To change the card dimensions, adjust the `fixed_width` and `fixed_height` variables.
- For different font styles or sizes, modify the font loading section at the top of `main.py`.
- To adjust the radius of the card's rounded edges, change the `radius` value in the `generate_rounded_mask` function call within the `create_canvas` function.

## Dependencies

- Python 3.x
- PIL (Python Imaging Library)

## Contributing

If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License

This project is free software; you can redistribute it and/or modify it. Please refer to the project's license for more details.
