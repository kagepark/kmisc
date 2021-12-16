#Kage park
import os

class COLOR:
    def __init__(self,**opts):
       self.color_db=opts.get('color',{'blue': 34, 'grey': 30, 'yellow': 33, 'green': 32, 'cyan': 36, 'magenta': 35, 'white': 37, 'red': 31})
       self.bg_color_db=opts.get('bg',{'cyan': 46, 'white': 47, 'grey': 40, 'yellow': 43, 'blue': 44, 'magenta': 45, 'red': 41, 'green': 42})
       self.attr_db=opts.get('attr',{'reverse': 7, 'blink': 5,'concealed': 8, 'underline': 4, 'bold': 1})

    def Color_code(self,name,default=None):
       return self.color_db.get(name,default)

    def Background_code(self,name,default=None):
       return self.color_db.get(name,default)

    def Attr_code(self,name,default=None):
       return self.color_db.get(name,default)

    def Get(self,color,mode='color',default=None):
       color_code=None
       if mode == 'color':
           color_code=self.Color_code(color,default=default)
       elif mode in ['background','bg']:
           color_code=self.Background_code(color,default=default)
       elif mode in ['attr','attribute']:
           color_code=self.Attr_code(color,default=default)
       return color_code

    def String(self,msg,color,bg=False,attr=False,mode='shell'):
       if mode in ['html','HTML']:
           if bg:
               return '''<p style="background-color: {}">{}</p>'''.format(format(color,msg))
           else:
               return '''<font color={}>{}</font>'''.format(color,msg)
       else:
           if bg:
               color_code=self.Get(color,mode='bg',default=None)
           elif attr:
               color_code=self.Get(color,mode='attr',default=None)
           else:
               color_code=self.Get(color,default=None)
           if color_code is None:
               return msg
           if os.getenv('ANSI_COLORS_DISABLED') is None:
               reset='''\033[0m'''
               fmt_msg='''\033[%dm%s'''
               msg=fmt_msg % (color_code,msg)
               return msg+reset

