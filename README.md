# CPAG

CPAG is the one and only command line based python posterizer with pixel art capabilities.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need these 2 packages to be able to run CPAG:

Python > 3.0, 

PILLOW

You can install python from this [link](https://www.python.org/ftp/python/3.7.3/python-3.7.3-amd64.exe) for windows, or you could use the commands below for linux:

```
sudo apt-get install python3.7
```


You can install the package PILLOW by using this command:

```
pip3 install PILLOW
```


## Using the code

Using `Palette.py` is pretty easy, just run the code, type the name of the image (in the folder /Inputs/) that you want to posterize and just wait. the images will be rendered in the folder /Outputs/ as rendered.png and palette.png.

Using `Posterizer.py` is a little bit more intresting. if you run posterizer.py, a list of every image that starts with 'UI' in the folder /Inputs/ is posterized and put in the folder /Outputs/, but keep in mind that if you want to add an image to the /Inputs/ folder, you need to add the next number after you write 'UI'. (UI stands for user-image)

For details on how to use `CPAG.py` just run the app and you'll get a help dialogue. dont use any spaces for values!

## Built With

* [Python](https://www.python.org/) - The language used
* [PILLOW](https://pypi.org/project/Pillow/) - The Used package

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* *Programmer* - [ParsaShahzeidi](https://github.com/parsashahzeidi)

See also the list of [contributors](https://github.com/parsashahzeidi/CPAG/graphs/contributors) who participated in this project.

## License

This project is licensed under the UnLicense - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Thanks to Pixabay for their amazing library of free images
* Thanks to all the artists who worked on the images in /Inputs/, especially FunsizedCoke
* Thanks to you for 'potentially' starring the project.

### Attribution

This ReadMe is adapted from this [Readme Template][Template] by Github user: PurpleBooth,
Follow her at [This link][PurpleBooth]


[Template]: https://gist.github.com/PurpleBooth/109311bb0361f32d87a2
[PurpleBooth]: https://github.com/PurpleBooth


