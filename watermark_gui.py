# coding: utf-8

from tkinter import *
from PIL import Image, ImageTk
import json, os

class WaterMarkGui:
    def __init__(self):
        self.__main_win = None
        self.__input_images_path = None
        self.__input_img_btn = None
        self.__watermark_text = None
        self.__preview_btn = None
        self.__output_dir = None
        self.__preview_img_label = None
        self.__photo_image = None
        self.__win_width = 600
        self.__win_height = 600
        
    def create_main_gui(self):
        self.__main_win = Tk()
        win_width, win_height = self.__win_width, self.__win_height
        self.__create_window(win_width, win_height)
        row_index = 0
        self.__layout_input_images_row(row_index)

        row_index += 1
        self.__layout_output_directory_row(row_index)

        row_index += 1
        self.__layout_watermark_text_row(row_index)

        row_index += 1
        self.__layout_preview_image_region(row_index, win_width, win_height)

        # read protocol from "config.json"
        self.__read_protocol()

        # register exit event to save current protocol into "config.json" file
        self.__main_win.protocol("WM_DELETE_WINDOW", self.__exit_event)

    def get_images_to_process(self):
        return self.__input_images_path.get()

    def set_images_to_process(self, value):
        self.__input_images_path.set(value)

    def get_water_mark_text(self):
        return self.__watermark_text.get()

    def set_water_mark_text(self, value):
        return self.__watermark_text.set(value)

    def set_output_dir(self, value):
        self.__output_dir.set(value)

    def get_output_dir(self):
        return self.__output_dir.get()

    def show_preview_image(self, image_path = None, image_object = None):
        if image_path is not None:
            img_to_show = self.__resize_image(Image.open(image_path))
        elif image_object is not None:
            img_to_show = self.__resize_image(image_object)
        else:
            img_to_show = self.__resize_image( Image.new("RGBA", (self.__win_width // 2, self.__win_height), (255, 0, 0, 255)) )
        self.__preview_img_label['width'] = 500
        self.__preview_img_label['height'] = 500
        self.__preview_img_label['image'] = img_to_show

    def select_images_to_process(self):
        # Call file open window to select files or directory
        import tkinter.filedialog as filedialog
        filenames = filedialog.askdirectory()
        if filenames.strip():
            self.__input_images_path.set(filenames)

    def select_output_dir(self):
        import tkinter.filedialog as filedialog
        dir = filedialog.askdirectory()
        if dir.strip():
            self.__output_dir.set(dir)

    def bind_preview_btn_call_back(self, func):
        self.__preview_btn.bind("<ButtonRelease>", func)

    def __read_protocol(self):
        if os.path.exists("config.json"):
            with open("config.json", "r") as file:
                json_dict = json.load(file)
                self.set_images_to_process(json_dict['input_path'])
                self.set_water_mark_text(json_dict['watermark_text'])
                self.set_output_dir(json_dict['output_dir'])

    def __exit_event(self):
        json_dict = {}
        json_dict['input_path'] = self.get_images_to_process()
        json_dict['watermark_text'] = self.get_water_mark_text()
        json_dict['output_dir'] = self.get_output_dir()
        with open("config.json", "w") as file:
            json.dump(json_dict, file)
            self.__main_win.destroy()

    def __resize_image(self, img_obj):
        img_width, img_height = img_obj.size
        img_obj_to_show = None
        if img_width <= 500 and img_height <= 500:
            img_obj_to_show = img_obj
        elif img_width > img_height:
            scale_ratio = img_width / 500
            img_height_to_show = int(img_height / scale_ratio)
            img_obj_to_show = img_obj.resize((500, img_height_to_show), Image.ANTIALIAS)
        else:  # img_height > img_width
            scale_ratio = img_height / 500
            img_width_to_show = int(img_width / scale_ratio)
            img_obj_to_show = img_obj.resize((img_width_to_show, 500, Image.ANTIALIAS))
        self.__photo_image = ImageTk.PhotoImage(img_obj_to_show)
        return self.__photo_image
    
    def __create_window(self,width, height):
        screen_width = self.__main_win.winfo_screenwidth()
        screen_height = self.__main_win.winfo_screenheight()
        size = "%dx%d+%d+%d"%(width, height, (screen_width - width) / 2, (screen_height - height) / 2)
        print("size : ", size)
        self.__main_win.geometry(size)
    
    def __layout_input_images_row(self, row_index):
        # Controls in the input images select row
        Label(self.__main_win, text="输入图像：").grid(row = row_index, padx = 10, pady = 5)
        self.__input_images_path = StringVar("")
        input_entry = Entry(self.__main_win, textvariable = self.__input_images_path, width = 55)

        self.__input_img_btn = Button(self.__main_win, text="选择图像/目录", command = self.select_images_to_process)
        input_entry.grid(row = row_index, column = 1, columnspan = 3, padx = 5, pady = 5, sticky = W)
        self.__input_img_btn.grid(row = row_index, column = 4, padx = 5, pady = 5, sticky = W)
    
    def __layout_watermark_text_row(self, row_index):
        Label(self.__main_win, text="水印文字：").grid(row = row_index, padx = 10, pady = 5)
        self.__watermark_text = StringVar()
        entry = Entry(self.__main_win, textvariable = self.__watermark_text, width = 55)
        self.__preview_btn = Button(self.__main_win, text = "预览效果")
        
        entry.grid(row=row_index, column = 1, columnspan = 3, padx = 5, pady = 5, sticky = W)
        self.__preview_btn.grid(row = row_index, column = 4, padx = 5, pady = 5, sticky = W)

    def __layout_output_directory_row(self, row_index):
        Label(self.__main_win, text="输出目录").grid(row=row_index, padx = 10, pady = 5)
        self.__output_dir = StringVar()
        entry = Entry(self.__main_win, textvariable = self.__output_dir, width = 55)
        select_output_dir_btn = Button(self.__main_win, text = "输出目录", command = self.select_output_dir)

        entry.grid(row = row_index, column = 1, columnspan = 3, padx = 5, pady = 5, sticky = W)
        select_output_dir_btn.grid(row = row_index, column = 4, padx = 5, pady = 5, sticky = W)

    def __layout_preview_image_region(self, row_index, win_width, win_height):
        self.__preview_img_label = Label(self.__main_win)
        self.__preview_img_label.grid(row = row_index, columnspan = 5, rowspan = 5, padx = 10, pady = 5)
        
    def __get_preview_image(self, image_path = None, width = 300, height = 300):
        photo = None
        if image_path is None:
            photo = Image.new("RGBA", (width, height), (255, 0,0,255))
        else:
            with Image.open(image_path) as img:
                photo = img.resize((width, height), Image.ANTIALIAS)
        self.__photo_image = ImageTk.PhotoImage(photo)
        return self.__photo_image

'''
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
'''

def main():
    watermark_gui = WaterMarkGui()
    watermark_gui.create_main_gui()
    '''
    watermark_controller = WaterMarkController(watermark_gui)
    watermark_gui.bind_preview_btn_call_back(watermark_controller.preview_btn_callback)
    '''
    mainloop()

if __name__ == "__main__":
    main()


# In[ ]:



