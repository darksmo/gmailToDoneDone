gmailToDoneDone
===============

This is a mix of Javascript and Python hacks to turn a Gmail Email into a [DoneDone](http://www.getdonedone.com) issue.

![Screenshot DoneDone IT!](images/screenshot.png)

Why?
----

This project is here because I often copy-paste content of e-mails into DoneDone. I need to quickly create a ticket out of an email for one member of my team. Have a look at my [blog post](http://www.savio.dimatteo.it/blog/entry/6) to know more about it!

Tested with
----------

What follows has been tested exclusively on:

- Google Chrome
- running on Debian Linux
- Python 2.7.3

Disclaimer
----------
This software is provided by Savio Dimatteo "as is" and "with all faults." Savio Dimatteo makes no representations or warranties of any kind concerning the safety, suitability, lack of viruses, inaccuracies, typographical errors, or other harmful components of this software. There are inherent dangers in the use of any software, and you are solely responsible for determining whether this software is compatible with your equipment and other software installed on your equipment. You are also solely responsible for the protection of your equipment and backup of your data, and Savio Dimatteo will not be liable for any damages you may suffer in connection with using, modifying, or distributing this software.

How To
------

1. Generate and Add the Bookmarklet

    - Copy the content of bookmarklet.js and paste it into a bookmarklet generator website like [this one](http://chriszarate.github.io/bookmarkleter/).
    
    - Click "convert to bookmarklet"
    
    - Drag the "Link!" at the bottom of the page into your bookmark bar.

2. Add your Done Done credentials

    - open doneDoneServer.py, scroll down and fill up the followings:
    
            domain = "<YOUR DONE DONE DOMAIN HERE>"
            token = "<YOUR API TOKEN GOES HERE>"
            username = "<YOUR DONEDONE USERNAME>"
            password = "<YOUR DONEDONE PASSWORD>"
            serverPort = 8011
            projectName = "<PROJECT NAME IN WHICH TO POST ISSUE>"
            fixerName = "<FIXER NAME>"
            testerName = "<TESTER NAME>"

    - pip install --user flask
    - pip install --user requests

3. Run the server

    - python ./doneDoneServer.py
    
4. Log into [GMail](http://www.gmail.com)

5. Click your bookmarklet to enable the DoneDone button

    - your gmail search icon should become orange, meaning the bookmarklet is enabled:
    
    ![Screenshot of orange search icon](images/orangesearch.png)

6. Now Open an email

    - an orange "DoneDone IT!" button should appear before the email subject

7. Click the DoneDone IT! button

    - **click it once!** &rarr; it should send the subject and the body to the listening python server.
    - the subject of the email will be the title of the issue
    - the body of the email will be the description of the issue
    - TIP: if you highlight a text before pressing that button, the selected text will be added into the DoneDone body instead!




