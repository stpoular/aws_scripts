'''
Code adapted from: https://www.coursera.org/learn/integrate-aws-sdk

This code reads image files from an S3 bucket,
builds a grid image and saves it to S3, returning a link for it.
'''


import os
import io
import math
import tempfile
import sys
from PIL import Image

from utils.s3_utils import dir_s3_bucket, read_s3_file, write_s3_file, create_presigned_url

MINUTE_THRESHOLD = 10


def main():
    if len(sys.argv) != 4:
        print("Usage: python demo_s3bucket.py [source-bucket] [destination-bucket] [expiration_minutes]")
        print("Example: python demo_s3bucket.py source-images-us-west-2-273783422348989348 destination-images-us-west-2-34433243423443 5")
        return

    source_bucket = sys.argv[1]
    destination_bucket = sys.argv[2]
    expiration_minutes = int(sys.argv[3])
    print('source_bucket: ', source_bucket)
    print('destination_bucket: ', destination_bucket)
    print('expiration_minutes: ', expiration_minutes)
    if expiration_minutes > MINUTE_THRESHOLD:
        print(f'Error: expiration_minutes should be < {MINUTE_THRESHOLD}')
        return

    tile_size = 100

    source_images, image_count = dir_s3_bucket(source_bucket)

    # calc the height, width of the grid
    tiles_width = math.floor(math.sqrt(image_count))
    tiles_height = math.ceil(image_count / tiles_width)

    print(f"Converting: {image_count} source images.\n\n Creating: {tiles_width} x {tiles_height} grid.\n\n")

    destination_image = Image.new(mode="RGB", size=(tiles_width * tile_size, tiles_height * tile_size))
    for y in range(tiles_height):
        for x in range(tiles_width):
            if source_images:
                filename = source_images.pop()

                # Read the S3 file
                image_data = read_s3_file(source_bucket, filename)

                img = Image.open(io.BytesIO(image_data))
                img_width = img.size[0]
                img_height = img.size[1]
                # crop the image to a square the length of the shorted side
                crop_square = min(img.size)
                img = img.crop(((img_width - crop_square) // 2,
                                (img_height - crop_square) // 2,
                                (img_width + crop_square) // 2,
                                (img_height + crop_square) // 2))
                img = img.resize((tile_size, tile_size))
                # draw the image onto the destination grid
                destination_image.paste(img, (x*tile_size, y*tile_size))

    # save the output image to a temp file
    temp_file = tempfile.NamedTemporaryFile(suffix='.jpg').name
    destination_image.save(temp_file)
    print(f"Creating temp file {temp_file}")

    # save the image to an S3 file and return a temporary url for it
    destination_key = os.urandom(16).hex() + ".jpg"
    write_s3_file(temp_file, destination_bucket, destination_key)
    presigned_url = create_presigned_url(destination_bucket, destination_key, expiration_minutes)
    print(f"Presigned URL: {presigned_url}\n")


if __name__ == '__main__':
    main()
