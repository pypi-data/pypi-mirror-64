import click
import pkgutil
import os
import re

@click.option('--image-name', default='dockerized-app', help='Image name to use for build.')
@click.option('--port', type=int, default=-1, help='The port to run the image on.')
@click.command()
def cli(image_name, port):
    """Example script."""
    #Identify app type
    app_type = identify_app_type()
    click.echo(app_type + ' app detected')

    #Generate Dockerfile
    click.echo('Generating Dockerfile...')
    if (app_type == 'JAVA_SPRING_BOOT'):
        found_file = ''
        for filename in os.listdir('target/'):
            if re.search('.*\.jar', filename):
                found_file = filename
                break
        if(found_file == ''):
            click.Abort('No jar file present. Make sure your target/ contains a jar file')
        text = pkgutil.get_data(__name__, "templates/Java.Dockerfile").decode()
    open("Dockerfile", "w").writelines([l for l in text])
    click.echo('Dockerfile generated')

    #Port was not passed in argument, set default values based on app_type
    if (port == -1):
        if (app_type == 'JAVA_SPRING_BOOT'):
            port = 8080

    #Build Docker image
    click.echo('Building Docker image...')
    os.system('docker build -t {} .'.format(image_name))
    click.echo('Built image {}'.format(image_name))

    #Run Docker image
    click.echo('Running Docker image...')
    os.system('docker run -p {}:{} {}'.format(port, port, image_name))

def identify_app_type():
    """Identify the project language to build Dockerfile"""
    return 'JAVA_SPRING_BOOT'

# if __name__ == '__main__':
#     # Identify app type
#     app_type = identify_app_type()
#     click.echo(app_type + ' app detected')
#
#     # Generate Dockerfile
#     click.echo('Generating Dockerfile...')
#     if (app_type == 'JAVA_SPRING_BOOT'):
#         if (not os.path.exists('target/*.jar')):
#             click.Abort('No jar file present. Make sure your target/ contains a jar file')
#     open("Dockerfile", "w").writelines([l for l in open("templates/Java.Dockerfile").readlines()])
#     click.echo('Dockerfile generated')
#
#     # Port was not passed in argument, set default values based on app_type
#     port = 8080
#     image_name = 'dockerize-image'
#
#     # Build Docker image
#     click.echo('Building Docker image...')
#     os.system('docker build -t {} .'.format(image_name))
#     click.echo('Built image {}'.format(image_name))
#
#     # Run Docker image
#     click.echo('Running Docker image...')
#     os.system('docker run -p {}:{} {}'.format(port, port, image_name))