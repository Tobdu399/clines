# CLines

Simple tool for calculating the lines of the files found in the current directory

---  
  
### Setup  
- Open a terminal with administrator privileges and go to the directory where you downloaded this repo.  
- In the directory, there should be at least two files, `clines.exe` and `setup.ps1`. If you are using command prompt, type in `powershell .\setup.ps1` or if you are using PowerShell, just type in `.\setup.ps1`  
- Follow the steps, which will be shown in your terminal as you run the script  
  
---  
  
### Usage  
- If you set up the program successfully with the setup instructions above, you should now be able to run the program by simply typing `clines` in your terminal.  
- After that, you should see a list of files, and the amount of lines in the file
- If you decided not to add the program to path, or the setup failed, you have to type the full path to the `clines.exe` program in order to use it.
### Note  
- The calculation speed depends on the file size in the directory. If a file has more than few thousand lines, the calculation process may take few seconds
