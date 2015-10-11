# -*- coding: utf8 -*-

def getch():
    import termios
    import sys, tty
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()

def write_display(lcd, content):
    '''
        Escreve o conteúdo no display, efetuando quebras de linha se necessário
    '''
    lcd.command(lcd.CMD_Display_Control)
    index = 0
    if len(content) > 16:
        words = content.split()
        word_lengths = [len(w) for w in words]
        for i in xrange(1,len(words)+1):
            if sum(word_lengths[:i])+i-1 > 16:
                index = i-1
                break
        if index == 0: #Se a primeira palavra tem mais de 16 letras
            index = 1
        lcd.clear()
        lcd.writeString(' '.join(words[:index]))
        lcd.setPosition(2,0)
        lcd.writeString(' '.join(words[index:]))
    else:
        lcd.clear()
        lcd.writeString(content)

    lcd.command(lcd.CMD_Display_Control | lcd.OPT_Enable_Display)


def read_input(lcd):
    '''
    Lê uma entrada do usuário até que ele digite ENTER
    '''
    c = ''
    s = ''
    while c != '\r':
        c = getch()
        if c.isalnum():
            s += c
            lcd.writeChar('*')
    return s