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

def read_input():
    '''
    Lê uma entrada do usuário até que ele digite ENTER
    '''
    c = getch()
    s = ''
    while c != '\r':
        s += c
        c = getch()
        #Faz alguma coisa a cada pressionamento de tecla
    return s