import tkinter as tk

from matplotlib.backend_bases import MouseButton
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class display_window:

    # figure_canvases = []
    left_button_pressed = False
    right_button_pressed = False
    mouse_dragged = False
    isopen = True

    def __init__(self, count, top, width = 1024, height = 768):
        # self.figure_canvases = []
        self.figure_dict = {}
        self.top = top
        self.display_level = tk.Toplevel(top)
        self.display_level.title('显示' + str(count))
        screen_width = self.display_level.winfo_screenwidth()
        screen_height = self.display_level.winfo_screenheight()
        init_position_x = int((screen_width - width) / 2)
        init_position_y = int((screen_height - height) / 2)
        position = str(width) + 'x' + str(height) + '+' + str(init_position_x) + '+' + str(init_position_y)
        self.display_level.geometry(position)
        self.display_level.protocol('WM_DELETE_WINDOW', self.close)

        self.x_offset = 120
        self.y_offset = 10
        self.figures_interval = 10
        new_figure_button = tk.Button(self.display_level, text='新建图表', command=self.new_figure_callback)
        new_figure_button.place(x=5, y=5)

        delete_figure_button = tk.Button(self.display_level, text = '删除图表', command=self.delete_figure_callback)
        delete_figure_button.place(x=5, y=50)

    # def new_figure_callback(self):
    #     figure_canvas = tk.Canvas(self.display_level, bg='white', cursor='cross')
    #     # figure_canvas.tag_bind
    #     self.figure_canvases.append(figure_canvas)
    #     # figure_canvas.create_rectangle(10, 10, 110, 110)
    #     figure_canvas.pack()
    #     # 绑定鼠标左键事件，交由processMouseEvent函数去处理，事件对象会作为参数传递给该函数
    #     figure_canvas.bind(sequence="<Button-1>", func=self.processMouseEvent)
    #     # print(figure_canvas)
    #     figure_canvas.config()

    def new_figure_callback(self):
        
        fig = Figure(figsize=(3, 2), dpi=100)
        fig_plot = fig.add_subplot(111)
        fig_plot.grid()
        if self.figure_dict:
            fig.gca().axes.set_xlim(self.x_axes_left_value, self.x_axes_right_value)
        
        self.x_axes_left_value, self.x_axes_right_value = fig.gca().axes.get_xlim()
        # print(self.x_axes_left_value, self.x_axes_right_value)
        
        
        # fig.canvas.callbacks.connect('button_press_event', self.callback)
        # print(type(fig_plot))
        

        figure_canvas = FigureCanvasTkAgg(fig, self.display_level)
        figure_widget = figure_canvas.get_tk_widget()
        figure_widget.config(highlightthickness = 2, highlightbackground = "white", cursor='cross')
        
        # figure_widget.bind(sequence="<Button-1>", func=self.pressMouseEvent, add = '+')
        # figure_widget.bind(sequence="<B1-Motion>", func=self.moveMouseEvent, add='+')
        toolbar = NavigationToolbar2Tk(figure_canvas, self.display_level)
        
        # figure_canvas.place(x)
        # figure_canvas.pack()
        figure_canvas.mpl_connect('button_press_event', self.mouse_press_callback)
        figure_canvas.mpl_connect('motion_notify_event', self.mouse_motion_callback)
        figure_canvas.mpl_connect('button_release_event', self.mouse_release_callback)

        # self.figure_canvases.append(figure_canvas)
        data_keys = []
        self.figure_dict[figure_widget] = {
            "fig": fig, 
            "fig_plot": fig_plot, 
            "figure_canvas": figure_canvas, 
            "toolbar": toolbar, 
            "data_keys": data_keys
        }
        self.arrange_figures(self.x_offset, self.y_offset, self.figures_interval)
        
    def mouse_press_callback(self, me):
        # print("me=", type(me))  # me= <class>
 
        # print("位于屏幕", me.x_root, me.y_root)
        # print("位于窗口", me.x, me.y)
        # print("位于窗口", me.canvas.get_tk_widget())
        # print(me.button)

        self.active_convas_widget = me.canvas.get_tk_widget()
        # print(self.figure_dict[self.active_convas_widget]['fig_plot'].get_xticks())
        

        if me.button == MouseButton.LEFT:
            self.left_button_pressed = True
            self.x_line = me.xdata
            # print(self.x_line)
            for figure_widget in self.figure_dict.keys():
                # self.figure_dict[figure_widget]['xline'] = self.figure_dict[figure_widget]['fig_plot'].axvline(x = self.x_line, color = 'r')
                # self.figure_dict[figure_widget]['figure_canvas'].draw()
                if figure_widget == self.active_convas_widget:
                    # figure_convas.config(bd = 10)
                    figure_widget.config(highlightthickness = 2, highlightbackground = "#AF6A6A")
                else:
                    # figure_convas.config(bd = 2)
                    figure_widget.config(highlightthickness = 2, highlightbackground = "white")
            try:
                # print(self.data_dict[self.data_key][-1])
                # me.widget.create_text(60, 30, text = self.data_key)
                if self.data_key not in self.figure_dict[self.active_convas_widget]['data_keys']:
                    self.figure_dict[self.active_convas_widget]['data_keys'].append(self.data_key)
                    self.figure_dict[self.active_convas_widget]['fig_plot'].plot(self.data_dict[self.data_key], label = self.data_key)
                    # self.figure_dict[self.active_convas_widget]['fig_plot'].legend(self.figure_dict[self.active_convas_widget]['data_keys'])
                    self.figure_dict[self.active_convas_widget]['fig_plot'].legend()
                    self.figure_dict[self.active_convas_widget]['figure_canvas'].draw()
                del self.data_key
            except AttributeError:
                pass

    def mouse_motion_callback(self, me):
        if self.left_button_pressed:
            self.mouse_dragged = True
            self.set_all_x_lim()


    def mouse_release_callback(self, me):
        if me.button == MouseButton.LEFT and not self.mouse_dragged:
            # if not self.mouse_dragged:
            for figure_widget in self.figure_dict.keys():
                try:
                    self.figure_dict[figure_widget]['xline'].remove()
                except KeyError:
                    pass
                except ValueError:
                    pass
                if self.x_line:
                    self.figure_dict[figure_widget]['xline'] = self.figure_dict[figure_widget]['fig_plot'].axvline(x = self.x_line, color = 'r')
                self.figure_dict[figure_widget]['figure_canvas'].draw()
                # self.figure_dict[figure_widget]['xline'].draw()
        # print('release')
        self.left_button_pressed = False
        self.mouse_dragged = False
        self.set_all_x_lim()
        # print(self.x_axes_left_value, self.x_axes_right_value)

    def set_all_x_lim(self):
        x_left, x_right = self.figure_dict[self.active_convas_widget]['fig'].gca().axes.get_xlim()
        # print(x_left, x_right, self.x_axes_left_value, self.x_axes_right_value)
        if (self.x_axes_left_value, self.x_axes_right_value) != (x_left, x_right):
            # print(self.figure_dict.keys())
            for it in self.figure_dict.keys():
                if it != self.active_convas_widget:
                    self.figure_dict[it]['fig'].gca().axes.set_xlim(x_left, x_right)
                    self.figure_dict[it]['figure_canvas'].draw()
                    # print(self.figure_dict[it]['fig'].gca().axes.set_xlim(x_left, x_right))

                    # print(it)
                    # print(self.figure_dict[it]['fig'].gca().axes.get_xlim())
            self.x_axes_left_value = x_left
            self.x_axes_right_value = x_right

    # 处理鼠标事件，me为控件传递过来的鼠标事件对象
    def pressMouseEvent(self, me):
        print("me=", type(me))  # me= <class>
 
        print("位于屏幕", me.x_root, me.y_root)
        print("位于窗口", me.x, me.y)
        print("位于窗口", me.widget)

        self.active_convas_widget = me.widget
        
        # for figure_convas in self.figure_canvases:
        for figure_widget in self.figure_dict.keys():
            if figure_widget == self.active_convas_widget:
                # figure_convas.config(bd = 10)
                figure_widget.config(highlightthickness = 2, highlightbackground = "#AF6A6A")
            else:
                # figure_convas.config(bd = 2)
                figure_widget.config(highlightthickness = 2, highlightbackground = "white")
        try:
            # print(self.data_dict[self.data_key][-1])
            # me.widget.create_text(60, 30, text = self.data_key)
            if self.data_key not in self.figure_dict[self.active_convas_widget]['data_keys']:
                self.figure_dict[self.active_convas_widget]['data_keys'].append(self.data_key)
                self.figure_dict[self.active_convas_widget]['fig_plot'].plot(self.data_dict[self.data_key])
                self.figure_dict[self.active_convas_widget]['figure_canvas'].draw()
            del self.data_key
        except AttributeError:
            pass

    def moveMouseEvent(self, me):
        # me.widget.create_text(200, 200, text = 'moving')
        print('move')

        

    def delete_figure_callback(self):
        try:
            # self.figure_canvases[-1].destroy()
            self.active_convas_widget.destroy()
            self.figure_dict[self.active_convas_widget]['toolbar'].destroy()
            # self.figure_canvases.remove(self.active_convas)
            self.figure_dict.pop(self.active_convas_widget)
            self.arrange_figures(self.x_offset, self.y_offset, self.figures_interval)
        except IndexError:
            pass
        except AttributeError:
            pass
        except ValueError:
            pass
        except ZeroDivisionError:
            pass
        except KeyError:
            pass

    def arrange_figures(self, x_offset, y_offset, figures_interval):
        figures_area_width = self.display_level.winfo_width() - x_offset - figures_interval
        figures_area_height = self.display_level.winfo_height() - y_offset - figures_interval
        figure_count = len(self.figure_dict)
        figure_width = figures_area_width
        figure_height = (figures_area_height - figures_interval * (figure_count - 1)) / figure_count
        # for i, it in enumerate(self.figure_canvases):
        for i, it in enumerate(self.figure_dict.keys()):
            it.config(height = figure_height, width = figure_width)
            it.place(x = x_offset, y = y_offset + i * (figure_height + figures_interval))
            self.figure_dict[it]['toolbar'].place(x=x_offset + 3, y=y_offset + i * (figure_height + figures_interval) + 3, width=200, height=40)


    def close(self):
        self.display_level.destroy()
        self.isopen = False

    def get_data(self, data):
        self.data_dict = data

    def get_data_key(self, key):
        self.data_key = key