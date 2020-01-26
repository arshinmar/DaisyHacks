# DaisyHacks

This repository is made for our submission into the Daisy Intelligence 2020 Hackathon.

### Team

The team consists of Haoran Jayce Wang and Arsh Kadakia.

### Main Problem:

Teams will be provided with a set of scanned images of flyers for a grocery retailer, a product dictionary that contains names of all the products, and a sample output file with some examples. Each flyer is for a weekly promotion and includes a start and an end date. Each flyer consists of multiple pages which in turn contain a varying number of ad-blocks. Each ad-block has a picture of the product, name and description of the product, price, unit of measurement (lb/kg or number of items), promotional discount, and additional tags such as organic, fresh, non-GMO, gluten-free, etc.

The product dictionary contains just the names of products. Participants must match ad-blocks using the descriptions on the flyer and the product dictionary and then extract the additional information for each ad-block. The output should be saved in a csv (comma delimited) format (taken from the main problem statement).

### How Did We Solve the Problem?

There were steps that were executed in a pipeline to solve the problem. In this GitHub, the main pipeline and its basis functions are included.

## 1. Segment into individual product blocks.

This step was performed through OpenCV image processing. The text portions of the flyers were dilated and blurred. Then, thresholding was performed to get the main text regions, which became highlighted in white. Finally, rectangular contours were taken on the blurred out regions. As a result, rectangles were formed around the main text boxes. The coordinates of these boxes were utilised in the next step.

## 2. Use Google Cloud Vision API to recognize text.

Thanks to Google Cloud's available credit to use their variety of APIs, we were able to use a state-of-the-art algorithm at no cost. With the Google Cloud Vision API, we were able to conduct text recognition into the segmented product blocks. The output ended up being a string of words that corresponded to the text within the images.

## 3. Do data processing to glean necessary insights as per the challenge.

After strings were outputted, analysis was required to get the necessary parts of the required output from the challenge.

Some of these outputs were easy to do, such as the checking of the word organic or the units of the product. These required a simple search through the string.

Other parts, such as getting the main price and discount price, were slightly harder. These required intuitive searching through the string, such as checking the string directly after the word 'SAVE'

## 4. Outputting the information to a CSV

This was done using the Pandas library, which allowed for easy writing with the variables from the pipeline forming the rows.

### What Did We Learn From This Project?

We learned how state-of-the-art APIs from Google and other companies can be used under the correct circumstances to perform certain jobs. 

Furthermore, we learned how to use image processing through libraries such as OpenCV to highlight certain features such as edges and contours. 

Other libraries that we gained further understanding of included OS,argparse,pandas, etc.

## Questions?

Contact Arsh Kadakia or Jayce Wang (collaborators on this repository) for further details. 
