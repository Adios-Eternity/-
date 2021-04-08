import random, string
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

class ImageCode:
    # 生成用于绘制字符串的随机颜色
    def rand_color(self):
        red = random.randint(32, 200)
        green = random.randint(22, 255)
        blue = random.randint(0, 200)
        return red, green, blue
    #生成4位随机字符串
    def gen_text(self):
        #sample用于一个大的列表或者字符串中，随机取得N个字符来构建一个子列表
        list = random.sample(string.ascii_letters+string.digits, 4)
        return ''.join(list)

    #画一些干扰线，其中draw位PIL中的ImageDraw对象
    def draw_lines(self, draw, num, width, height):
        for num in range(num):
            x1 = random.randint(0, width/2)
            y1 = random.randint(0, height/2)
            x2 = random.randint(0, width)
            y2 = random.randint(height/2, height)
            draw.line(((x1,y1),(x2,y2)),fill='black', width=2)
    #绘制验证图片
    def draw_verify_code(self):
        code = self.gen_text()
        width, height = 120, 50  #设定图片大小，可根据实际需求调整
        im = Image.new('RGB', (width, height), 'white')
        #选择使用何种字体以及字体大小
        font = ImageFont.truetype(font='arial.ttf', size=40)
        draw = ImageDraw.Draw(im)
        #绘制字符串
        for i in range(4):
            draw.text((5 + random.randint(-3, 3) + 23 * i, 5 + random.randint(-3, 3)),
                      text=code[i], fill=self.rand_color(), font=font)
        #绘制干扰线
        self.draw_lines(draw, 2, width, height)
        im.show()  #如需临时调试，可以直接将生成的图片显示出来
        return im, code

    #生成图片验证码并返回给控制器
    def get_code(self):
        image, code = self.draw_verify_code()
        buf = BytesIO()
        image.save(buf, 'jpeg')
        bstring = buf.getvalue()
        return code, bstring

#发送邮箱验证码
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

#发送QQ邮箱验证码， 参数位收件箱地址和随机生成的验证码
def send_email(receiver, ecode):
    sender = 'zzy <1224723717@qq.com>'
    #定义发送邮箱的内容，支持HTML标签和CSS样式
    content = f"<br/>欢迎注册果园系统账号，您的邮箱验证码位：<span style='color:red;font-size:20px;'>{ecode}</span>,请复制到窗口完成注册<br/>"
    #实例化邮件对象，并指定邮件的关键信息
    message = MIMEText(content, 'html', 'utf-8')
    #指定邮件的标题，同样使用utf-8编码
    message['Subject'] = Header('果园系统', 'utf-8')
    message['Form'] = sender #指定发件人信息
    message['To'] = receiver #指定收件人邮箱地址

    smtpobj = SMTP_SSL('smtp.qq.com') #建议与QQ邮件服务器的连接
    #通过你的邮箱账号和获取收到的授权码登录QQ邮箱
    smtpobj.login(user='1224723717@qq.com', password='wfmmabvqoqtibadc')
    #指定发件人，收件人和邮件内容
    smtpobj.sendmail(sender, receiver, str(message))
    smtpobj.quit()
def gen_email_code():
    str = random.sample(string.ascii_letters + string.digits, 6)
    return ''.join(str)
