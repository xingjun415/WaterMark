
# coding: utf-8

# In[ ]:

from tkinter import *
from PIL import Image, ImageTk

class WaterMarkGui:
    def __init__(self):
        self.__main_win = None
        self.__input_images_path = None
        self.__input_img_btn = None
        self.__watermark_text = None
        self.__preview_btn = None
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
        self.__layout_watermark_text_row(row_index)

        row_index += 1
        self.__layout_preview_image_region(row_index, win_width, win_height)

    def get_images_to_process(self):
        return self.__input_images_path.get()

    def set_images_to_process(self, value):
        self.__input_images_path.set(value)

    def get_water_mark_text(self):
        return self.__watermark_text.get()

    def set_water_mark_text(self, value):
        return self.__watermark_text.set(value)

    def show_preview_image(self, image_path = None, image_object = None):
        if image_path is not None:
            img_to_show = self.__resize_image(Image.open(image_path))
        elif image_object is not None:
            img_to_show = self.__resize_image(image_object)
        else:
            img_to_show = self.__resize_image( Image.new("RGBA", (self.__win_width // 2, self.__win_height), (255, 0, 0, 255)) )
        self.__preview_img_label['image'] = img_to_show

    def select_images_to_process(self):
        # Call file open window to select files or directory
        import tkinter.filedialog as filedialog
        filenames = filedialog.askdirectory()
        self.__input_images_path.set(filenames)

    def bind_preview_btn_call_back(self, func):
        self.__preview_btn.bind("<ButtonRelease>", func)
                
    def __resize_image(self, img_obj):
        self.__photo_image = ImageTk.PhotoImage(img_obj)
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
    
    def __layout_preview_image_region(self, row_index, win_width, win_height):  
        #self.image = "lena.jpg"
        #photo = self.__get_preview_image("lena.jpg")
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

import weakref, os
from watermark import WaterMark
class WaterMarkController:
    def __init__(self, win_gui):
        self.__supported_images = ['.png', '.jpg']
        self.__win_gui = weakref.ref(win_gui)

    def preview_btn_callback(self, evt):
        print("preview_btn_callback is called")
        images_to_process = self.get_images_to_process()
        print(images_to_process)

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
        return [directory + filename for filename in filenames if self.__is_support_img(filename)]

    def __is_support_img(self,  filename):
        return os.path.splitext(filename)[1] in self.__supported_images

img = "lena.jpg"
watermark_gui = WaterMarkGui()

def change_image(evt):
    print("directory to process : ", watermark_gui.get_images_to_process())
    '''
    global img
    img = "lena.jpg" if img is None else None
    watermark_gui.show_preview_image(img)
    '''
def main():
    watermark_gui.create_main_gui()
    watermark_controller = WaterMarkController(watermark_gui)
    watermark_gui.bind_preview_btn_call_back(watermark_controller.preview_btn_callback)
    mainloop()

if __name__ == "__main__":
    main()


# In[ ]:



