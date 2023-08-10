import os
import shutil
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageOps

# Path to the RussoOne-Regular font file
GENERAL_FONT_PATH = "./font/RussoOne-Regular.ttf"

# Load different font sizes for versatility
general_font_small = ImageFont.truetype(GENERAL_FONT_PATH, 60)
general_font_large = ImageFont.truetype(GENERAL_FONT_PATH, 80)

fixed_width = 500 
fixed_height = 500

def get_resized_logo(canvas_width, opacity=0.5):
    """
    Resize the logo image while maintaining aspect ratio and adjusting opacity.
    
    Args:
        canvas_width (int): The target width for the resized logo.
        opacity (float): Desired opacity level for the logo (default is 0.5).
    
    Returns:
        Image: Resized logo image with adjusted opacity.
    """
    logo_path = "logo/logo.png"
    logo = Image.open(logo_path)
    
    # Resize the logo while maintaining aspect ratio
    logo = logo.resize((canvas_width, int((canvas_width / logo.width) * logo.height)))
    
    # Adjust the opacity of the logo to the specified value
    logo = logo.convert("RGBA")
    data = list(logo.getdata())
    for i, item in enumerate(data):
        data[i] = item[:-1] + (int(item[3] * opacity),)
    logo.putdata(data)
    
    return logo


def get_resized_background_logo(canvas_width):
    logo_path = "logo/logo.png"
    logo = Image.open(logo_path)

    # Resize the logo while maintaining aspect ratio
    logo = logo.resize((canvas_width, int((canvas_width / logo.width) * logo.height)))

    # Adjust the opacity of the logo for the composite background
    logo = logo.convert("RGBA")
    data = list(logo.getdata())
    for i, item in enumerate(data):
        data[i] = item[:-1] + (int(item[3] * 0.5),)  # 50% opacity for composite
    logo.putdata(data)
    
    return logo

def get_character_images(character1, character2, fixed_width, fixed_height):
    """
    Load and resize images of two characters to a fixed width and height while maintaining aspect ratio.
    
    Args:
        character1 (str): Name of the first character.
        character2 (str): Name of the second character.
        fixed_width (int): The target width for the resized character renders.
        fixed_height (int): The target height for the resized character renders.
        
    Returns:
        tuple: Resized images of character1 and character2.
    """
    char1_image_path = os.path.join("renders", character1, "1.png")
    char2_image_path = os.path.join("renders", character2, "1.png")
    
    # Print the paths being accessed
    print(f"Accessing image from: {char1_image_path}")
    print(f"Accessing image from: {char2_image_path}")

    char1_image = Image.open(char1_image_path)
    char2_image = Image.open(char2_image_path)

    # Calculate new dimensions while maintaining aspect ratio
    new_width1 = int((fixed_height / char1_image.height) * char1_image.width)
    new_width2 = int((fixed_height / char2_image.height) * char2_image.width)

    if new_width1 > fixed_width:
        new_width1 = fixed_width
        new_height1 = int((fixed_width / char1_image.width) * char1_image.height)
    else:
        new_height1 = fixed_height

    if new_width2 > fixed_width:
        new_width2 = fixed_width
        new_height2 = int((fixed_width / char2_image.width) * char2_image.height)
    else:
        new_height2 = fixed_height

    # Resize images to fixed dimensions
    char1_image = char1_image.resize((new_width1, new_height1), True)
    char2_image = char2_image.resize((new_width2, new_height2), True)

    return char1_image, char2_image



def paste_gradient_on_canvas(canvas):
    """
    Paste a rotated gradient image onto the canvas using a mask.
    
    Args:
        canvas (Image): The canvas image onto which the gradient will be pasted.
        
    Returns:
        Image: Canvas image with the rotated gradient applied.
    """
    gradient_size = int((canvas.width**1 + canvas.height**2)**0.45)
    
    # Create gradient and rotate it by 45 degrees
    gradient = create_gradient(gradient_size, gradient_size)  # Missing function implementation
    rotated_gradient = gradient.rotate(45, expand=1)
    
    diagonal_length = (gradient_size**2 + gradient_size**2)**0.5
    
    # Create a mask from the rotated gradient and position variables
    mask = rotated_gradient.convert('L').point(lambda x: 255 if x > 0 else 0, mode='1')
    position_x = -int(diagonal_length / 2)
    position_y = position_x
    
    # Paste rotated gradient onto the canvas using the mask
    canvas.paste(rotated_gradient, (position_x, position_y), mask)
    
    return canvas
def paste_light_blue_square(canvas):
    """
    Paste a rotated light blue square onto the canvas using a mask.
    
    Args:
        canvas (Image): The canvas image onto which the blue square will be pasted.
        
    Returns:
        Image: Canvas image with the rotated blue square applied.
    """
    gradient_size = int((canvas.width**1 + canvas.height**2)**0.45)
    
    # Create a light blue square and rotate it
    blue_square = Image.new('RGB', (gradient_size, gradient_size), (173, 216, 230))
    rotated_blue = blue_square.rotate(-47, expand=1)
    
    diagonal_length = (gradient_size**2 + gradient_size**2)**0.5
    blue_position_x = -int(diagonal_length / 2) + 10
    blue_position_y = blue_position_x + 5
    
    # Create a mask from the rotated blue square
    blue_mask = rotated_blue.convert('L').point(lambda x: 255 if x > 0 else 0, mode='1')
    
    # Paste rotated blue square onto the canvas using the mask
    canvas.paste(rotated_blue, (blue_position_x, blue_position_y), blue_mask)
    
    return canvas

def paste_character_renders(canvas, char1_image, char2_image):
    """
    Paste character renders onto the canvas at specific positions.
    
    Args:
        canvas (Image): The canvas image onto which the renders will be pasted.
        char1_image (Image): Image of the first character.
        char2_image (Image): Image of the second character.
        
    Returns:
        Image: Canvas image with character renders pasted.
    """
    # Check if char1_image is 'ptx' or 'gold'
    if char1_image in ['ptx', 'gold']:
        char2_image = char1_image  # Set char2_image to be the same as char1_image
        
        # Calculate the center position for the first unique character on the canvas
        center_x = (canvas.width - char1_image.width) // 2
        canvas.paste(char1_image, (center_x - 300, 0))
        
        # Calculate the position for the second unique character on the canvas
        center_x = (canvas.width - char2_image.width) // 2
        canvas.paste(char2_image, (500, char1_image.height))
        
    else:
        canvas.paste(char1_image, (50, 0), char1_image if char1_image.mode == 'RGBA' else None)
        if char2_image:
            canvas.paste(char2_image, (char1_image.width - 50, 0), char2_image if char2_image.mode == 'RGBA' else None)
  
    
    return canvas

def draw_winner_info_on_canvas(canvas, winner_name, rank_number):
    """
    Draw winner information on the canvas.
    
    Args:
        canvas (Image): The canvas image on which the winner information will be drawn.
        winner_name (str): Name of the winner.
        rank_number (int): The rank/position of the winner.
        
    Returns:
        Image: Canvas image with winner information drawn.
    """
    draw = ImageDraw.Draw(canvas)
    font = general_font_small
    min_font_size = 30  # set a minimum font size
    
    left_margin = 50  # Define left border
    right_margin = canvas.width - 50  # Define right border
    max_width = right_margin - left_margin  # maximum allowable width for the text
    
    # Calculate text bounding box for winner's name
    temp_image = Image.new('RGBA', (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)
    bbox = temp_draw.textbbox((0,0), winner_name, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # Reduce font size if text width exceeds max width, but don't go below minimum font size
    while text_width > max_width and font.size > min_font_size:
        font = ImageFont.truetype(GENERAL_FONT_PATH, font.size - 5)  # reduce font size by 5 units
        bbox = temp_draw.textbbox((0,0), winner_name, font=font)
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    # If text width still exceeds max width after reaching minimum font size, break the text into multiple lines
    if text_width > max_width:
        winner_name = "\n".join(winner_name.split(maxsplit=1))
    
    # Calculate text position for winner's name
    text_x = (canvas.width - text_width) // 2
    text_y = canvas.height - 80 - (text_height // 2 if "\n" in winner_name else 0)  # Adjust position if text is on multiple lines
    
    # Ensure text doesn't exceed left or right margins. If it does, adjust `text_x` accordingly.
    if text_x < left_margin:
        text_x = left_margin
    elif text_x + text_width > right_margin:
        text_x = right_margin - text_width
    
    # Draw winner's name using calculated position
    draw_text_with_effects(draw, text_x, text_y, winner_name, font, fill="white", outline="black", shadow=(255, 220, 220), thickness=3)
    
    # Draw ranking number using larger font
    large_font = general_font_large
    draw_text_with_effects(draw, 10, 10, f"{rank_number}.", large_font, fill="white", outline="black", shadow=(255, 220, 220), thickness=3)
    
    return canvas





def draw_text_with_effects(draw, x, y, text, font, fill, outline, shadow, thickness=3, shadow_offset=(4, 4)):
    """
    Draws text with an outline and a drop shadow.
    
    Args:
        draw (ImageDraw.Draw): The drawing context.
        x (int): x-coordinate of text position.
        y (int): y-coordinate of text position.
        text (str): Text to be drawn.
        font (ImageFont): Font to be used.
        fill (tuple): RGB tuple for text color.
        outline (tuple): RGB tuple for outline color.
        shadow (tuple): RGB tuple for shadow color.
        thickness (int): Thickness of the outline.
        shadow_offset (tuple): (x, y) offsets for the shadow.
        
    Returns:
        None
    """
    # Draw the shadow
    draw.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow)
    
    # Draw the text multiple times with offsets to create the outline
    for offset_x in range(-thickness, thickness + 1):
        for offset_y in range(-thickness, thickness + 1):
            draw.text((x + offset_x, y + offset_y), text, font=font, fill=outline)
    
    # Draw the original text
    draw.text((x, y), text, font=font, fill=fill)

def draw_rectangles_on_canvas(canvas):
    """
    Draw rounded rectangles on the canvas with different colors and positions.
    
    Args:
        canvas (Image): The canvas image on which the rectangles will be drawn.
        
    Returns:
        Image: Canvas image with drawn rounded rectangles.
    """
    draw = ImageDraw.Draw(canvas)
    rect_height = 100
    rect_width = canvas.width + 10
    rect_start_x = (canvas.width - rect_width) / 2 + 30
    rect_end_x = rect_start_x + rect_width
    rect_bottom_y = canvas.height - (0.02 * canvas.height)
    rect_top_y = rect_bottom_y - rect_height
    yellow_offset_x = canvas.width * 0.1
    yellow_offset_y = rect_height * 0.05
    
    # Draw rounded rectangle in yellow
    draw.rounded_rectangle([rect_start_x + yellow_offset_x, rect_top_y + yellow_offset_y, rect_end_x + yellow_offset_x, rect_bottom_y + yellow_offset_y], radius=20, fill=(255,255,0))
    
    # Draw rounded rectangle in dark blue
    draw.rounded_rectangle([rect_start_x, rect_top_y, rect_end_x, rect_bottom_y], radius=20, fill=(0,0,139))
    
    return canvas

def create_gradient(width, height):
    """
    Create a gradient image using pastel rainbow colors.
    
    Args:
        width (int): Width of the gradient image.
        height (int): Height of the gradient image.
        
    Returns:
        Image: Gradient image with pastel rainbow colors.
    """
    # Define pastel rainbow colors
    colors = [
        (255, 102, 102),      # Pastel Red
        (255, 178, 102),     # Pastel Orange
        (255, 255, 102),     # Pastel Yellow
        (178, 255, 102),     # Pastel Green
        (102, 178, 255),     # Pastel Blue
        (178, 102, 255),     # Pastel Indigo
        (255, 102, 178)      # Pastel Violet
    ]
    
    # Create an empty gradient image
    gradient = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(gradient)
    
    # Draw the gradient
    for y in range(height):
        r, g, b = get_color_at(colors, y / height)  # Missing function implementation
        draw.line((0, y, width, y), fill=(r, g, b))
    
    return gradient

def get_color_at(colors, position):
    """
    Get interpolated color at a specific position between two colors.
    
    Args:
        colors (list): List of RGB colors for interpolation.
        position (float): Position between 0 and 1 for interpolation.
        
    Returns:
        tuple: Interpolated RGB color.
    """
    num_colors = len(colors)
    idx1, idx2 = int(position * (num_colors - 1)), int(position * (num_colors - 1)) + 1
    alpha = position * (num_colors - 1) - idx1
    
    if idx2 == num_colors:
        return colors[-1]
    
    col1 = colors[idx1]
    col2 = colors[idx2]
    
    r = int(col1[0] * (1 - alpha) + col2[0] * alpha)
    g = int(col1[1] * (1 - alpha) + col2[1] * alpha)
    b = int(col1[2] * (1 - alpha) + col2[2] * alpha)
    
    return r, g, b

def generate_rounded_mask(size, radius=30):
    """
    Generate a rounded rectangle mask.
    
    Args:
        size (tuple): Width and height of the desired mask.
        radius (int): Radius of the rounded corners.
    
    Returns:
        Image: A mask image with rounded corners.
    """
    width, height = size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=255)
    return mask

def compile_images():
   
    # Load the images
    images = [Image.open(f'rankings/{i}.png') for i in range(1, 9)]
    
    # Composite dimensions
    comp_width, comp_height = 1920, 1080
    # Create a blank composite image
    composite = Image.new('RGBA', (comp_width, comp_height), (0, 0, 0, 0))
    
    # Add the new background logo
    bg_logo = get_resized_logo(int(comp_width/2), opacity=0.8)  # 0.8 is 80% opacity
    composite.paste(bg_logo, (0, (comp_height - bg_logo.height) // 2), bg_logo)

    # Determine the size for the first image
    img1_width = int(comp_width/2.6)
    img1_height = int(comp_height/2.2)
    images[0] = images[0].resize((img1_width, img1_height))

    # Determine the size for images 2-4
    img24_width = int(img1_width/2)
    img24_height = int(img1_height/1.5)
    for i in range(1, 4):
        images[i] = images[i].resize((img24_width, img24_height))

    # Determine the size for images 5-8
    img58_width = int(img24_width/1.5)
    img58_height = int(img24_height/1.3)
    for i in range(4, 8):
        images[i] = images[i].resize((img58_width, img58_height))
    

    
    # Paste image 1 on the left
    y_position_1 = (comp_height - img1_height) // 2
    composite.paste(images[0], (0, y_position_1))
    
    # Paste images 2-4 on the right of image 1, in a row (horizontally)
    x_start_24 = img1_width + 5
    y_position_24 = y_position_1 - 20
    for i in range(1, 4):
        composite.paste(images[i], (x_start_24, y_position_24))
        x_start_24 += img24_width + 15

    # Paste images 5-8 below images 2-4, in a row (horizontally)
    x_start_58 = img1_width + 50
    y_position_58 = y_position_24 + img24_height
    for i in range(4, 8):
        composite.paste(images[i], (x_start_58, y_position_58))
        x_start_58 += img58_width + 20
    
    # Save the composite image
    composite.save('rankings/composite.png')
    print("Composite image saved to: rankings/composite.png")


def create_canvas(char1_image, char2_image, winner_name, rank_number):
    """
    Create a composite image canvas with fixed dimensions and various elements.
    
    Args:
        char1_image (Image): Image of the first character.
        char2_image (Image): Image of the second character.
        winner_name (str): Name of the winner.
        
    Returns:
        Image: Composite canvas image.
    """
    # Adjust the character image sizes to fit the new card dimensions
    char1_image = char1_image.resize((fixed_width // 2, fixed_height), True)
    char2_image = char2_image.resize((fixed_width // 2, fixed_height), True)
    
    # Create a canvas with fixed dimensions
    canvas = Image.new('RGBA', (fixed_width, fixed_height), (0, 0, 0, 255))
    
    # Calculate the positions for logo and other elements
    logo = get_resized_logo(fixed_width, opacity=0.5)  # 0.5 is 50% opacity
    canvas.paste(logo, (0, (canvas.height - logo.height) // 2), logo) 
    canvas = paste_light_blue_square(canvas)
    canvas = paste_gradient_on_canvas(canvas)
    canvas = paste_character_renders(canvas, char2_image, char1_image)
    canvas = draw_rectangles_on_canvas(canvas)
    canvas = draw_winner_info_on_canvas(canvas, winner_name, rank_number)
    # Create a rounded rectangle mask
    rounded_mask = generate_rounded_mask(canvas.size, radius=30)
    canvas.putalpha(rounded_mask)

    return canvas


def main():
    """
    Main function to create a series of composite images based on user input.
    """
    if os.path.exists("rankings"):
        shutil.rmtree("rankings")
    
    # Scan renders folder
    character_files = os.listdir("renders")
    available_characters = [os.path.splitext(file)[0] for file in character_files]

    # Create the "rankings" folder if it doesn't exist
    if not os.path.exists("rankings"):
        os.makedirs("rankings")

    # Check if ranking.txt exists
    if os.path.exists("ranking.txt"):
        with open("ranking.txt", "r") as file:
            lines = file.readlines()
            for rank, line in enumerate(lines, 1):
                winner_name, character1, character2 = map(str.strip, line.split(","))
                
                if character1 in ['ptx', 'gold'] and character2 == "blank":
                    character2 = character1
                    character1 = "blank"

                char1_image, char2_image = get_character_images(character1, character2, fixed_width, fixed_height)
                canvas = create_canvas(char1_image, char2_image, winner_name, rank)


                # Save the resulting image to the "rankings" folder
                output_filename = f"rankings/{rank}.png"
                canvas.save(output_filename)
                print(f"Image saved to: {output_filename}")

    else:
        # Loop to generate 8 composite images with rankings
        for rank in range(8, 0, -1):
            while True:  # Loop until valid characters are entered or user types 'END'
                # Prompt user for input
                winner_name = input(f"Enter the {ordinal_number(rank)} place winner's name (or type 'END' to exit): ")

                if winner_name.upper() == "END":
                    break

                character1 = input(f"Name of Character 1 (Choose from: {', '.join(available_characters)}): ").lower()

                if character1 not in ['ptx', 'gold']:
                    character2 = input(f"Name of Character 2 (Choose from: {', '.join(available_characters)}): ").lower()
                else:
                    character2 = "blank"

                char1_image, char2_image = get_character_images(character1, character2, fixed_width, fixed_height)
                canvas = create_canvas(char1_image, char2_image, winner_name, rank)


                # Save the resulting image to the "rankings" folder
                output_filename = f"rankings/{rank}.png"
                canvas.save(output_filename)
                print(f"Image saved to: {output_filename}")

                break  # Exit the while loop

    # Compile the images into one composite image
    compile_images()
def ordinal_number(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

if __name__ == "__main__":
    main()
