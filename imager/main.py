from sys import argv
from PIL import Image
import typer

app = typer.Typer()


@app.command()
def convert_to_rgb(input_image_file: str, output_name: str = "output", show_only: bool = False):
        input_name_parts = input_image_file.split('.')
        output_name_file = f"{output_name}.{input_name_parts[1]}"
        with Image.open(input_image_file) as image:
            if image.mode == 'RGBA':
                output_image = Image.new("RGBA", image.size, "WHITE")
                output_image.paste(image, (0, 0), image)
                output_image.convert("RGB")
                if show_only:
                    output_image.show()
                else:
                    output_image.save(output_name_file, input_name_parts[1].upper())

            else:
                print(f'cannot yet handle image in mode {image.mode}')


@app.command()
def show_image(input_image_file: str):
    
    with Image.open(input_image_file) as image:
        print(image.mode)
        image.show()


if __name__ == '__main__':
    app()
