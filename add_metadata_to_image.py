import piexif

def add_metadata_tags(image_file, input_signal_properties):
    # Load the EXIF data from the image file
    exif_data = piexif.load(image_file)
    
    # Convert the input signal properties to a string
    input_signal_string = ", ".join([f"{key}={value}" for key, value in input_signal_properties.items()])
    
    # Encode the string in UTF-16
    input_signal_bytes = input_signal_string.encode("utf-16")
    
    # Store the input signal properties as XPKeywords tag
    exif_data["0th"][piexif.ImageIFD.XPKeywords] = input_signal_bytes
    
    # Convert the EXIF data to bytes
    exif_bytes = piexif.dump(exif_data)
    
    # Insert the EXIF data back to the image file
    piexif.insert(exif_bytes, image_file)
