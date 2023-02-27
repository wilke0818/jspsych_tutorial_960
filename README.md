# **MIT 9.60 Tutorial**: Online Psychophysics Experiments

This is a tutorial on how to build an online visual behavioral experiment. It covers:

1. Using a free, open-source JavaScript framework ([jsPsych](https://www.jspsych.org/7.3/)) to create behavioral experiments that run in a web browser
2. Hosting an experiment on the web via [Athena web scripts](https://scripts.mit.edu/web/)

With just these pieces, it can be quite straightforward to collect data from huge numbers of participants using crowd-sourcing platforms such as [Prolific](https://www.prolific.co) and [Amazon mTurk](https://www.mturk.com). For 9.60 projects, you will have the option (and some funding) to collect participants from online crowd-sourcing platforms, but it is not required. A well-designed web browser experiment will also make high-quality data collection from friends, classmates, and colleagues **much easier and faster**. The purpose of this tutorial is to show you how easy [jsPsych](https://www.jspsych.org/7.3/) makes it to build online behavioral experiments that go way beyond what is possible with simple survey platforms (i.e., Google Forms). A few features of well-designed visual psychophysics experiments that are easy to implement include:
- Present stimuli for a fixed period of time
- Randomize trial order
- Collect reaction times
- Option to provide feedback on trials

**For the in-class tutorial, please bring your computer and whatever device you use for kerberos two-factor authentification (i.e., your cellphone).**

<br>

# **Setup** *(please complete these steps before the tutorial)*


***NOTE:** these steps may well be the most complicated part of building an online experiment, especially if you have never worked with a remote server before. Nonetheless, please attempt to follow these steps and bring any issues / questions to class. The TAs will be happy to help.*

<br>

1. If you do not already have it installed on your local machine, install the [Visual Studio Code (VSCode)](https://code.visualstudio.com/download) text editor.

<br>

2. Within VSCode, install the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension. This can be done by going to the "Extensions" tab and searching for "ms-vscode-remote.remote-ssh". This extension will enable VSCode to make an SSH connection from your local machine to the Athena web server, allowing you to directly edit files on Athena with VSCode (rather than using a command-line editor or constantly transferring files back and forth).

<br>

3. Follow these steps to connect to the [Athena web server](https://sipb.mit.edu/doc/using-athena/) and enable [web scripts](https://scripts.mit.edu/web/):
    * Open a terminal on your local machine and run the command `ssh kerberos@athena.dialup.mit.edu` (replacing `kerberos` with your kerberos ID) to initiate an SSH connection to the Athena web server. Enter your kerberos password and two-factor authentication as prompted:
        ```
        mark@my_local_machine:~ % ssh msaddler@athena.dialup.mit.edu
        msaddler@athena.dialup.mit.edu's password: 
        Duo two-factor login for msaddler

        Enter a passcode or select one of the following options:

        1. Phone call to XXX-XXX-XXXX
        2. SMS passcodes to XXX-XXX-XXXX

        Passcode or option (1-2): 1
        Success. Logging you in...
        ```
    * This will land you in your home directory on Athena. The command `pwd` (*print working directory*) should produce something like:
        ```
        msaddler@green-building-tetris:~$ pwd
        /afs/athena.mit.edu/user/m/s/msaddler
        ```
    * Enable [web scripts](https://scripts.mit.edu/web/) for your personal Athena account by running the commands `add scripts` and `signup-web`. Enabling web scripts is necessary because we will be building a dynamic (non-static) website for your experiment.
        ```
        msaddler@green-building-tetris:~$ add scripts
        msaddler@green-building-tetris:~$ signup-web

        Would you like to sign up:
        1. Your personal Athena account
        2. A locker that you control (a club, a course, etc)
        If you do not understand this question, you should answer '1'.
        Please enter either '1' or '2' (without quotes): 1
        /bin/attach: /afs/athena.mit.edu/user/m/s/msaddler attached to /mit/msaddler for filesystem msaddler
        /bin/attach: /afs/athena.mit.edu/user/m/s/msaddler attached to /mit/msaddler for filesystem msaddler

        == SUCCESS ==
        msaddler is now signed up for the web script service.
        ```
    * This will create a `web_scripts` folder in your home directory that is visible to the web. Let's put something in it:
        ```
        $ echo "You have reached the mit.scripts.edu homepage of $(whoami)" > ~/web_scripts/index.html
        ```
        This command writes the string "You have reached the mit.scripts.edu homepage of {kerberos}" to a file called `index.html` in your `web_scripts` directory. Files in this directory can be accessed from the web (mine is [https://msaddler.scripts.mit.edu/index.html](https://msaddler.scripts.mit.edu/index.html)). Note that `index.html` is a special filename reserved for a website's homepage. If you follow a URL to a directory (e.g., [https://msaddler.scripts.mit.edu](https://msaddler.scripts.mit.edu)) without specifying a file, it will automatically redirect you to the `index.html` file.

<br>

4. Modify permissions to allow VSCode to connect to Athena and to let your website read/write data:
    * Within your Athena home directory, we need to add a line to your `~/.bashrc.mine` file to allow VSCode to remotely edit files ([Athena documentation](https://sipb.mit.edu/doc/using-athena/)). This can be achieved with the command below:
        ```
        msaddler@green-building-tetris:~$ echo "find ~/.vscode-server/ -name 'vscode-remote-lock.$(whoami).*' -delete" >> ~/.bashrc.mine
        ```
    * You can check that a line was added to your `~/.bashrc.mine` file with `cat` command:
        ```
        msaddler@green-building-tetris:~$ cat ~/.bashrc.mine
        find ~/.vscode-server/ -name 'vscode-remote-lock.msaddler.*' -delete
        ```
    * For your experiment website to read and write data to the web server, we must give read/write access to the `web_scripts` directory. This is done with the following three commands:
        ```
        msaddler@green-building-tetris:~$ cd ~/web_scripts
        msaddler@green-building-tetris:~/web_script$ fs sa . system:anyuser read
        msaddler@green-building-tetris:~/web_script$ athrun scripts fssar daemon.scripts write
        ```

<br>

5. End your terminal's SSH connection to Athena using the `exit` command or `Ctrl-D`.

<br>

6. Follow [these instructions](https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host) to make a new SSH connection to Athena via the **Remote - SSH extension in VSCode**.
    * For `ssh user@hostname`, you will use `ssh {kerberos}@athena.dialup.mit.edu` with your own kerberos. If VSCode does not automatically detect that Athena is a Linux server, you may need to manually select Linux when prompted.
    * You should be prompted for your kerberos password and two-factor authentification in the VSCode search bar.
    * Once successfully connected, you should be able to open your `web_scripts` folder in VSCode.
    * Within that folder, you should see the `index.html` file that was created in the last part of **Step #3**. Editing the `index.html` file will change what you see when you visit your scripts.mit.edu homepage (e.g., https://msaddler.scripts.mit.edu). Note that updates may take a couple minutes to appear on the web.

<br>

7. Make a copy of of this Github repository on both your local machine and in your Athena `web_scripts` folder.
    * If you are familiar with Github and comfortable [setting up SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh#platform-all), I would recommend using `git clone` in the command line to clone this repository on both your local machine and in your Athena `web_scripts` folder.
    * Otherwise, you can simply download this Github repository to your local machine and then copy the directory over to Athena.
        * There are multiple ways to [transfer files between your local machine and Athena](http://kb.mit.edu/confluence/pages/viewpage.action?pageId=3907182). One easy way is with the `rsync` command in your local terminal:
        ```
        $ rsync -rav jspsych_tutorial_960 {kerberos}@athena.dialup.mit.edu:~/web_scripts
        ```
        * This command will copy your local directory `jspsych_tutorial_960` to `~/web_scripts/jspsych_tutorial_960` on Athena.

<br>

8. Once you have made the directory `~/web_scripts/jspsych_tutorial_960` on Athena, it should be accessible from the web. Please visit your copy of [https://msaddler.scripts.mit.edu/jspsych_tutorial_960](https://msaddler.scripts.mit.edu/jspsych_tutorial_960) and confirm that it looks like mine.

<br>

# **Contents**

* [0_hello_world.html](0_hello_world.html) : anatomy of an html file + jsPsych basics (timeline and plugins)
* [1_beginner.html](1_beginner.html) : toy image classification experiment + printing/downloading data locally
* [2_intermediate.html](2_intermediate.html) : timeline variables and nested timelines + writing data to server
* [3_advanced.html](3_advanced.html) : programatically generating timeline variables + pre-loading images + feedback
* [4_expert.html](4_expert.html) : fancier plugins and extensions (mouse-tracking / sorting) + integration with Prolific
* [template.html](template.html) : **blank experiment for you to fill in during the tutorial**
* [util.js](util.js) : some helpful JavaScript functions that can be called within html files
* [write_data.php](write_data.php) : PHP script that can receive data from a webpage and write it to file

<br>

# **Helpful resources**
- [Documentation for jsPsych](https://www.jspsych.org/) (**most helpful resource for actually coding your experiment webpage**)
    - [jsPsych tutorials](https://www.jspsych.org/7.3/tutorials/rt-task/)
    - [Overview of plugins in jsPsych](https://www.jspsych.org/7.3/overview/plugins/)
    - [Storing and manipulating data in jsPsych](https://www.jspsych.org/7.3/overview/data/) 
- [Documentation for scripts.mit.edu](https://scripts.mit.edu/web/) (particularly helpful [FAQs](https://scripts.mit.edu/faq/))
- [Brief documentation for using Athena to host a website](https://sipb.mit.edu/doc/using-athena/)
- [Kaggle](https://www.kaggle.com/datasets), a great place to find and download image datasets for machine learning
- [Hugging Face](https://huggingface.co/datasets), another great place to find and download image datasets for machine learning
    - Example images in this repository were taken from [https://huggingface.co/datasets/poolrf2001/FaceMask/tree/main](https://huggingface.co/datasets/poolrf2001/FaceMask/tree/main)
