import io
from sys import argv
from PIL import Image, ImageCms
import typer

app = typer.Typer()


@app.command()
def convert_to_rgb(input_image_file: str, output_name: str = "output", show_only: bool = False, jpeg: bool = False):
        input_name_parts = input_image_file.split('.')
        file_type = 'jpeg' if jpeg else input_name_parts[1]
        output_name_file = f"{output_name}.{file_type}"
        
        with Image.open(input_image_file) as image:
            if image.mode == 'RGBA':
                white_image = Image.new("RGB", image.size, "WHITE")
                white_image.paste(image, (0, 0), image)
                output_image = white_image.convert("RGB")
                if show_only:
                    output_image.show()
                else:
                    output_image.save(output_name_file, file_type)

            elif image.mode == 'CMYK':
                icc = image.info.get('icc_profile', None)
                if icc:
                    io_handle = io.BytesIO(icc)
                    src_profile = ImageCms.ImageCmsProfile(io_handle)
                    dest_profile = ImageCms.createProfile('sRGB')
                    output_image = ImageCms.profileToProfile(image, src_profile, dest_profile, outputMode='RGB')
                    if image.info.get('icc_profile', '') != output_image.info.get('icc_profile', ''):
                        if show_only:
                            output_image.show()
                        else:
                            output_image.save(output_name_file, 
                                                format=file_type.upper(),
                                                quality=100,
                                                icc_profile=output_image.info.get('icc_profile', ''))
                    else:
                        print('Could not convert image in CMYK mode')
            else:
                print(f'cannot yet handle image in mode {image.mode}')


@app.command()
def show_image(input_image_file: str):
    
    with Image.open(input_image_file) as image:
        print(image.mode)
        image.show()

@app.command()
def show_details(input_image_file: str):
    with Image.open(input_image_file) as image:
        print(f'Mode: {image.mode}')
        print(f'Format: {image.format}')

if __name__ == '__main__':
    app()
