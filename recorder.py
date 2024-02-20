from PIL import Image


class Recorder:
    def __init__(self, filename, extension="gif", fps=60):
        self.__extension = extension
        self.__filename = filename
        self.__duration = 1 / fps * 1000  # ms
        self.__fname = f"{self.__filename}.{self.__extension}"
        self.__images = list()

    def capture(self, img, size):
        self.__images.append(Image.frombytes("RGBA", size, img))

    def store(self):
        if len(self.__images) == 0:
            return
        self.__images[0].save(
            self.__fname,
            save_all=True,
            append_images=self.__images[1:],
            duration=self.__duration,
            loop=0,
        )