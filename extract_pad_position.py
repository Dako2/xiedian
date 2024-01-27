from PIL import Image
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Function to find the center of the contour
def find_contour_center(contour):
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
    return (cX, cY)




# Open the image file
img_path = 'footprint.png'

# Load the image in grayscale
image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Thresholding the image to get the contours
_, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)

# Finding contours in the image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# Dictionary to hold the center of each contour
contour_centers = {}

for contour in contours:
    # Get the center of the contour
    cX, cY = find_contour_center(contour)
    
    # Approximate the contour to a polygon to check for numbers (as they have more corners)
    approx = cv2.approxPolyDP(contour, 0.04 * cv2.arcLength(contour, True), True)
    
    # If the contour has more than 5 vertices, it might be a number
    if len(approx) > 5:
        # Get the bounding rectangle to isolate the number
        x, y, w, h = cv2.boundingRect(approx)
        
        # Crop and save the number area
        number_image = image[y:y+h, x:x+w]
        number_image_path = f'/number_{cX}_{cY}.png'
        cv2.imwrite(number_image_path, number_image)
        
        # Store the center in the dictionary with the image path as the key
        contour_centers[number_image_path] = (cX, cY)

# Calculate the image center
image_center = (image.shape[1]//2, image.shape[0]//2)

# Output the image center and the dictionary of contour centers
print(image_center, contour_centers)



# Load the image
image_color = cv2.imread(img_path)
image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)

# Invert the image to get white numbers on black background for better detection
image_gray = cv2.bitwise_not(image_gray)

# Use adaptive thresholding to isolate the numbers
thresh = cv2.adaptiveThreshold(image_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)

# Find contours of the numbers
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Function to find the center of the bounding box for a contour
def find_bounding_box_center(contour):
    x, y, w, h = cv2.boundingRect(contour)
    return (x + w//2, y + h//2)

# Find the centers of all contours
centers = [find_bounding_box_center(c) for c in contours]

# The image center can be calculated as the midpoint of the image dimensions
image_center = (image_color.shape[1] // 2, image_color.shape[0] // 2)

# Calculate the relative positions of each center from the image center
relative_positions = [(center[0] - image_center[0], center[1] - image_center[1]) for center in centers]

relative_positions, image_center
# We will use a more manual approach to identify the contours and filter out the noise.
# Define expected number width and height range based on the image scale and observations.
# These values are estimates and may need adjustment.
expected_number_width_min, expected_number_width_max = 10, 40
expected_number_height_min, expected_number_height_max = 20, 50

# Initialize a list to store the center points of valid number contours
valid_centers = []

# Loop over the contours to filter based on the expected size
for contour in contours:
    # Compute the bounding box of the contour
    x, y, w, h = cv2.boundingRect(contour)
    
    # Use the contour width and height to filter out contours that do not match the expected size of the numbers
    if (expected_number_width_min <= w <= expected_number_width_max and
            expected_number_height_min <= h <= expected_number_height_max):
        # This contour is likely to be a number, store its center point
        center_x, center_y = x + w//2, y + h//2
        valid_centers.append((center_x, center_y))

# Now calculate the relative positions of each valid center from the image center
relative_valid_positions = [(center[0] - image_center[0], center[1] - image_center[1]) for center in valid_centers]

relative_valid_positions

with Image.open(img_path) as img:
    plt.imshow(img)
    plt.axis('on') # 'off' turns off the axis, 'on' turns it on
    plt.show()

# Load the original image
original_image = cv2.imread(img_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

# Apply thresholding to create a mask with only the black frame pads
_, mask = cv2.threshold(gray_image, 100, 255, cv2.THRESH_BINARY_INV)

# Bitwise-and mask with the original image
black_frame_pads_only = cv2.bitwise_and(original_image, original_image, mask=mask)

# Convert the result back to RGB (OpenCV uses BGR by default)
black_frame_pads_only_rgb = cv2.cvtColor(black_frame_pads_only, cv2.COLOR_BGR2RGB)

# Save the resulting image
output_path = '/pads.png'
cv2.imwrite(output_path, black_frame_pads_only_rgb)

import cv2

# Initialize list to hold coordinates
pad_positions = []

# Mouse callback function to get the coordinates and draw a circle where the user clicks
def record_click(event, x, y, flags, param):
    # If the left mouse button was clicked, record the coordinates and draw a circle
    if event == cv2.EVENT_LBUTTONDOWN:
        pad_positions.append((x, y))
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Image", img)

# Read the image
img = cv2.imread(img_path)

# Create a window and bind the function to window
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", record_click)

# Display the image and wait for a click
cv2.imshow("Image", img)
cv2.waitKey(0)

# Close the window
cv2.destroyAllWindows()

# The pad_positions list now contains the coordinates of the clicks (i.e., the sensor pads)
print(pad_positions)

#output
#[(237, 217), (241, 104), (183, 641), (177, 534), (187, 394), (182, 236), (198, 90), (114, 645), (108, 538), (139, 399), (134, 240), (162, 95), (94, 432), (83, 324), (83, 225), (118, 121)]
#(158, 366) center


