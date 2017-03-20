import weakref, os
from watermark import WaterMark
class WaterMarkController:
    def __init__(self, win_gui):
        self.__supported_images = ['.png', '.jpg']
        self.__win_gui = weakref.ref(win_gui)

    def preview_btn_callback(self, evt):
        print("preview_btn_callback is called")
        images_to_process, text_as_watermark= self.get_images_to_process()
        print("Images to process : ", images_to_process)
        watermark = WaterMark()
        watermark.set_fill_rgba((100,100,100,100))
        image_processed = watermark.add_text_to_image(images_to_process[0], text_as_watermark)
        win_gui = self.__win_gui()
        win_gui.show_preview_image(image_object=image_processed)

    def get_images_to_process(self):
        win_gui = self.__win_gui()
        directory = win_gui.get_images_to_process()
        if not os.path.isdir(directory):
            import tkinter.messagebox as messagebox
            messagebox.showinfo(title="Error", message = "input directory is not supported")
            return
        print("directory is : ", directory)
        filenames = os.listdir(directory)
        print("filenames : ", filenames)
        return ([os.path.join(directory, filename) for filename in filenames if self.__is_support_img(filename)], win_gui.get_water_mark_text())

    def __is_support_img(self,  filename):
        return os.path.splitext(filename)[1] in self.__supported_images