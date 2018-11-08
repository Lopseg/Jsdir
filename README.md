# Jspathextractor

Jspathextractor is an Burp Suite extension that act as a midle betwen an js file and extractor.rb tool.

# Requirements 

To use this extension you need to do three things:
1. Download the extractor tool from jobert repository at https://github.com/jobertabma/relative-url-extractor

2. Edit the source code of this extension by inserting the right path to the tool and an writable path for a tmp file.

# Usage

Just import this extension in Extender Tab of Burp Suite.
Then when you see an Js file in any response of any server inside Burp suite, 
Just click on it with the right button, then choose "Send to Js scrapper".
Go to extender tab and see the results.

![My image](https://raw.githubusercontent.com/Lopseg/JsScrapper/master/output_jsscrapper.png)

# Notes

Feel free to help me improve this tool. Thank you Jobert.


*Lopseg*
