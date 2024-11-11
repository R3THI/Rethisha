import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import io
from rembg import remove

def remove_background(image):
    """Remove the background from the image using rembg."""
    # Convert the image to a byte stream and pass to rembg
    with io.BytesIO() as byte_io:
        image.save(byte_io, format="PNG")
        byte_data = byte_io.getvalue()

    output_data = remove(byte_data)
    return Image.open(io.BytesIO(output_data))

def add_sticker_border(image):
    """Add a rounded border or shadow effect to the image."""
    width, height = image.size
    # Create a background with transparency
    sticker = Image.new("RGBA", (width + 20, height + 20), (0, 0, 0, 0))
    sticker.paste(image, (10, 10))

    # Add a circular border effect
    draw = ImageDraw.Draw(sticker)
    border_radius = min(width, height) // 10
    draw.ellipse([(10, 10), (width + 10, height + 10)], outline="black", width=5)

    return sticker

def process_image(image):
    """Process the image: remove background and add sticker-like border."""
    # Remove background (optional)
    image = remove_background(image)
    # Add rounded sticker border effect
    image = add_sticker_border(image)
    return image

def main():
    st.title("Image to Sticker Translator")
    
    uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        # Load the image
        image = Image.open(uploaded_file)
        st.image(image, caption="Original Image", use_container_width=True)

        # Process the image to create a sticker
        sticker_image = process_image(image)
        
        # Show the transformed image
        st.image(sticker_image, caption="Sticker", use_container_width=True)

        # Allow users to download the sticker image
        buf = io.BytesIO()
        sticker_image.save(buf, format="PNG")
        buf.seek(0)
        st.download_button("Download Sticker", buf, "sticker.png", "image/png")

if __name__ == "__main__":
    main()
