import time
import pyautogui as pyi
import logging
import configparser
import pyperclip
import sys

con = configparser.ConfigParser()
con.read('./PingJiao/conf.ini', encoding='utf-8')
items = con.items('conf')
conf = dict(items)

if conf['level'] == 'DEBUG':
    logging.basicConfig(format='%(asctime)s - line:%(lineno)d] - %(levelname)s: %(message)s',
                        filename='./PingJiao/PingJiao.log',
                        filemode='a',
                        level=logging.DEBUG)
if conf['level'] == 'INFO':
    logging.basicConfig(format='%(asctime)s - line:%(lineno)d] - %(levelname)s: %(message)s',
                        filename='./PingJiao/PingJiao.log',
                        filemode='a',
                        level=logging.INFO)

sleep = int(conf['sleep_time'])
pyi.FAILSAFE = bool(conf['save_mode'])
pyperclip.copy(conf['remark'])

logging.info("欢迎使用评教系统~")
logging.debug("您已进入调试模式")
logging.debug("当前的屏幕大小为：" + str(pyi.size()))

pyi.alert(text='请确保打开教务系统的评教界面', title='提醒', button='OK')
a = pyi.prompt(text='请输入评教列数', title='输入评教列数', default='3')

if a is None or int(a) <= 0:
    pyi.alert(text='程序已结束', title='提醒', button='OK')
    logging.info('程序已结束')
    sys.exit()
try:
    time.sleep(sleep)
    loc = pyi.locateCenterOnScreen("./PingJiao/handle.png")
    if loc is None:
        pyi.alert(text='无法找到操作图片！', title='ERROR!', button='OK')
        logging.error('无法找到操作图片！')
        sys.exit()
    main_x = loc[0] - 18
    main_y = loc[1]

    for i in range(int(a)):
        time.sleep(sleep)
        logging.info(f"进行第{i + 1}次评教")
        main_yy = main_y + 26 * (i + 1)
        pyi.moveTo((main_x, main_yy), duration=0.1)
        pyi.click(clicks=1)
        time.sleep(sleep)

        locate = pyi.locateCenterOnScreen("./PingJiao/ended.png")
        if locate is not None:
            pyi.moveTo(locate, duration=0.1)
            pyi.click(clicks=1)
            logging.info('此课程已评教完成，退出')
            continue

        loc = pyi.locateCenterOnScreen("./PingJiao/remark_result.png")
        if loc is None:
            pyi.alert(text='无法找到评价结果图片！', title='ERROR!', button='OK')
            logging.error('无法找到评价结果图片！')
            sys.exit()
        ox, oy = 0, 0
        for ii in range(18):
            x = loc[0]
            y = loc[1] + 27 * (ii + 1)
            if ii == 0:
                ox = x + 55
                oy = y
            pyi.moveTo((ox, oy), duration=0.1)
            pyi.click(clicks=1)
            pyi.moveTo((x, y), duration=0.1)
            pyi.click(clicks=1)
            pyi.typewrite(conf['score'])
        loc = pyi.locateCenterOnScreen("./PingJiao/remark.png")
        if loc is None:
            pyi.alert(text='无法找到评语图片！', title='ERROR!', button='OK')
            logging.error('无法找到评语图片！')
            sys.exit()
        x = loc[0] + 60
        y = loc[1] + 5
        pyi.moveTo((x, y), duration=0.4)
        pyi.click(clicks=1)
        time.sleep(sleep)
        pyi.click(clicks=1)
        pyi.hotkey('Ctrl', 'v')
        loc = pyi.locateCenterOnScreen("./PingJiao/save.png")  # region参数限制查找范围，加快查找速度
        if loc is None:
            pyi.alert(text='无法找到保存图片！', title='ERROR!', button='OK')
            logging.error('无法找到保存图片！')
            sys.exit()
        x = loc[0]
        y = loc[1]
        pyi.moveTo((x, y), duration=0.1)
        pyi.click(clicks=1)
        time.sleep(sleep)
        ok_loc = pyi.locateCenterOnScreen("./PingJiao/ok.png")  # region参数限制查找范围，加快查找速度
        if ok_loc is None:
            pyi.alert(text='无法找到确定图片！', title='ERROR!', button='OK')
            logging.error('无法找到确定图片！')
            sys.exit()
        pyi.moveTo(*ok_loc, duration=0.1)
        pyi.click(clicks=1)
        pyi.moveTo((x + 50, y), duration=0.1)
        if bool(conf['is_ok']):
            a = pyi.prompt(text='请核实', title='请人工核实', default='OK')
            if a != 'OK':
                pyi.alert(text='程序已停止', title='提醒', button='OK')
                logging.info('程序已停止')
                sys.exit()
        pyi.click(clicks=1)
        time.sleep(sleep)
        pyi.moveTo(*ok_loc, duration=0.1)
        pyi.click(clicks=1)
        pyi.moveTo((x + 100, y), duration=0.1)
        pyi.click(clicks=1)
        logging.info('此课程已评教完成，退出')
    pyi.alert(text='程序已执行完毕', title='提醒', button='OK')
    logging.info('程序已执行完毕')
except pyi.FailSafeException as e:
    pyi.alert(text='安全模式终止', title='结束', button='OK')
    logging.info('安全模式终止')
    sys.exit()
except Exception as e:
    pyi.alert(text='其他问题错误，请联系管理员', title='ERROR!!!', button='OK')
    logging.error('其他问题错误，请联系管理员')
    sys.exit()
