from distutils.core import setup
import py2exe
    
Mydata_files = [('avrdude', ['avrdude\\avrdude.conf','avrdude\\avrdude.exe'])]
setup(windows=['atmega-uploader.py'],
      data_files = Mydata_files,
      options={"py2exe":{"unbuffered": True,
                         "optimize":2,
                         "excludes": ["email"]}})
