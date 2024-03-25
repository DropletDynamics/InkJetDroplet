import piexif

def add_metadata_tags(image_file, input_signal_properties):
    # Load the EXIF data from the image file
    exif_data = piexif.load(image_file)
    
    # Convert the input signal properties to a string
    input_signal_string = ", ".join([f"{key}={value}" for key, value in input_signal_properties.items()])
    # print(input_signal_string)
    # Encode the string in UTF-16
    input_signal_bytes = input_signal_string.encode("utf-16")
    # print(input_signal_bytes.decode("utf-16"))
    
    # Store the input signal properties as XPKeywords tag
    exif_data["0th"][piexif.ImageIFD.XPKeywords] = input_signal_bytes
    
    # Convert the EXIF data to bytes
    exif_bytes = piexif.dump(exif_data)
    
    # Insert the EXIF data back to the image file
    piexif.insert(exif_bytes, image_file)

def read_metadata_tags(image_file):
    # Load the EXIF data from the image file
	exif_data = piexif.load(image_file)
 
	# Extract the input signal properties tuple from XPKeywords tag
	input_signal_tuple = exif_data["0th"][piexif.ImageIFD.XPKeywords]

	# Convert the tuple to a UTF-16 encoded string
	input_signal_bytes = bytes(input_signal_tuple)

	# Decode the string using UTF-16 encoding
	input_signal_string = input_signal_bytes.decode("utf-16")

	# Split the string into a dictionary
	input_signal_properties = dict([tuple(item.split('=')) for item in input_signal_string.split(', ')])

	return input_signal_properties


# exampl ussage
# image_file = 'enhanced_image.jpg'

# # Define your input signal properties as a dictionary
# input_signal_properties = {"V1": 50, "V2": -60, "V3": 10, "w1": 27, "w2": 25, "w3": 26, "d1": 10, "d2": 20}
# # Call the function with your image file name and input signal properties
# add_metadata_tags(image_file, input_signal_properties)

# properties = read_metadata_tags(image_file)
# print(properties)
# Load the EXIF data from the image file
# exif_data = piexif.load(image_file)

# Print the XPKeywords tag
# print(exif_data["0th"][piexif.ImageIFD.XPKeywords])#.decode("utf-16")



# exif_dict = piexif.load(image_file)
# thumbnail = exif_dict.pop("thumbnail")
# if thumbnail is not None:
#     with open("thumbnail.jpg", "wb+") as f:
#         f.write(thumbnail)
# for ifd_name in exif_dict:
#     print("\n{0} IFD:".format(ifd_name))
#     for key in exif_dict[ifd_name]:
#         try:
#             print(key, exif_dict[ifd_name][key][:10])
#         except:
#             print(key, exif_dict[ifd_name][key])