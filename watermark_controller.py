import weakref, os
from watermark_algo import WaterMark
class WaterMarkController:
    def __init__(self, win_gui):
        self.__supported_images = ['.png', '.jpg']
        self.__win_gui = weakref.ref(win_gui)

    def preview_btn_callback(self, evt):
        print("preview_btn_callback is called")
        images_to_process, text_as_watermark, output_dir = self.get_images_to_process()
        print("Images to process : ", images_to_process)
        watermark = WaterMark()
        watermark.set_fill_rgba((100,100,100,100))
        image_processed = watermark.add_text_to_image(images_to_process[0], text_as_watermark)
        win_gui = self.__win_gui()
        win_gui.show_preview_image(image_object=image_processed)

    def save_images_processed(self, evt):
        print("Beging process images")
        images_to_process, watermark_text, output_dir = self.get_images_to_process()
        print("Images to process : ", images_to_process)
        print("watermark text : ", watermark_text)
        print("output directory : ", output_dir)
        print("dir : ", os.path.dirname(images_to_process[0]))
        filename, ext_name = os.path.splitext(os.path.basename(images_to_process[0]))
        print("file name : ", filename)
        print("ext name : ", ext_name)
        watermark = WaterMark()
        watermark.set_fill_rgba((100,100,100,100))
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        for image in images_to_process:
            print("Begin process file : ", image)
            image_proecessed = watermark.add_text_to_image(image, watermark_text)
            file_name, ext_name = os.path.splitext(os.path.basename(image))
            file_name += "_added_watermark" + ext_name
            watermark.save(image_proecessed, os.path.join(output_dir, file_name))
            print("finished process file : ", image)



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
        return ([os.path.join(directory, filename) for filename in filenames if self.__is_support_img(filename)],
                win_gui.get_water_mark_text(), win_gui.get_output_dir())

    def __is_support_img(self,  filename):
        return os.path.splitext(filename)[1] in self.__supported_images

from tkinter import *
def main():
    from watermark_gui import WaterMarkGui
    win_gui = WaterMarkGui()
    win_gui.create_main_gui()
    controller = WaterMarkController(win_gui)
    win_gui.bind_preview_btn_call_back(controller.save_images_processed)
    mainloop()

if __name__ == "__main__":
    main()