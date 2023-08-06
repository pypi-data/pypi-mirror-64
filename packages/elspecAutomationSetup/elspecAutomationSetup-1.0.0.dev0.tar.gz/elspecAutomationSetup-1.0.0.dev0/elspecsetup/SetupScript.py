##############################################
##                                          ##
##          Script version: 2.0.9           ##
##          Last update: 12.03.20           ##
##                                          ##
##############################################
import os

def main():
    Issues = ''
    command = 'python -m pip install -U pip setuptools'
    x = os.system(command)
    if not x == 0:
        print('##################################################')
        print('##################################################')
        print('##################################################')
        print('unable to update pip and setuptools. exiting test.')
        print('##################################################')
        print('##################################################')
        print('##################################################')
        exit()
    lib_list = ['pythonnet', 'pynput', 'numpy', 'matplotlib', 'scipy', 'paramiko'
        , 'oct2py', 'PyVISA', 'pyshark', 'modbus_tk' ,'pyserial', 'xpath-py'
        , 'py-dom-xpath-six', 'PILLOW', 'opencv-python', 'xlrd', 'pytz'
        , 'pandas', 'dominate', 'pdfkit', 'WxPython', 'elevate', 'PyMuPDF', 'tabula-py==1.4.3'
        , 'PySimpleGUI', 'logzero','dicttoxml', 'xmltodict']
    for lib in lib_list:
        command = 'pip install ' + lib
        x = os.system(command)
        if not x == 0:
            Issues += 'unable to install ' + lib + '.\n'
    if Issues == '':
        print('#################################\n')
        print('									\n')
        print('									\n')
        print('all installations are successful!\n')
        print('									\n')
        print('									\n')
        print('#################################\n')
    else:
        print('#################################################\n')
        print('													\n')
        print('													\n')
        print('some installations have failed. here is a list:! \n')
        print('													\n')
        print('													\n')
        print('													\n')
        print('													\n')
        print('#################################################\n')
        print(Issues)
    input('press any key to exit')


if __name__ == "__main__":
    main()