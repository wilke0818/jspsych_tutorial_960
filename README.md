# **MIT 9.60 Tutorial:** Online Psychophysics Experiments

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

# Setup

## **Before the tutorial, please attempt to complete the following:**

**NOTE:** *these setup steps may well be the most complicated part of building an online experiment, especially if you have never worked with a remote server before. Nonetheless, please attempt to follow these steps and bring any issues / questions to class. The TAs will be happy to help.*

1. Install [Visual Studio Code (VSCode)](https://code.visualstudio.com/download) if you do not already have it on your local machine. It is a very convenient text editor for code that will allow you to directly edit files on a remote server (i.e., on the Athena web server where your experiment website will be hosted).

2. Within VSCode, install the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension. This can be done by going to the Extensions tab > search "ms-vscode-remote.remote-ssh". This extension will enable VSCode to make an SSH connection from your local machine to the Athena web server, allowing you to directly edit files on Athena with VSCode (rather than using a command-line editor or constantly transferring files back and forth).

3. Connect to the [Athena web server](https://sipb.mit.edu/doc/using-athena/) and enable [web scripts](https://scripts.mit.edu/web/):
    * In your local machine's terminal (not VSCode), run the command `ssh kerberos@athena.dialup.mit.edu` (replacing `kerberos` with your kerberos ID) to initiate an SSH connection to the Athena web server.
    * Enter your kerberos password and two-factor authentication as prompted.
    * This should land you in your home directory on Athena. The command `pwd` (*print working directory*) should produce something like:
        ```
        msaddler@green-building-tetris:~$ pwd
        /afs/athena.mit.edu/user/m/s/msaddler
        ```
    * Enable [web scripts](https://scripts.mit.edu/web/) for your personal Athena account by running the following two commands. Enabling web scripts is necessary because we will be building a dynamic (non-static) website for your experiment.
        ```
        $ add scripts
        $ signup-web
        ```
    * This will make a `web_scripts` folder in your home directory that is visible to the web. Let's put something in it:
        ```
        $ echo "You have reached the mit.scripts.edu homepage of $(whoami)" > ~/web_scripts/index.html
        ```
    * You should now be able to access your scripts.mit.edu homepage from the web. Mine is [https://msaddler.scripts.mit.edu](https://msaddler.scripts.mit.edu).<br><br>

4. Setup  permissions to allow VSCode to connect to Athena and to let your website read/write data:
    * Within your Athena home directory, we need to add a line to your `~/.bashrc.mine` file to allow VSCode to remotely edit files ([Athena documentation](https://sipb.mit.edu/doc/using-athena/)). This can be achieved with the following one-line command:
        ```
        $ echo "find ~/.vscode-server/ -name 'vscode-remote-lock.$(whoami).*' -delete" > ~/.bashrc.mine
        ```
    * For your experiment website to read and write data to the web server, we must give read/write access to the `web_scripts` directory. This is done with the following three commands:
        ```
        $ cd ~/web_scripts
        $ fs sa . system:anyuser read
        $ athrun scripts fssar daemon.scripts write
        ```

5. End your terminal's SSH connection to Athena using the `exit` command or `Ctrl-D`.<br>

6. Follow [these instructions](https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host) to make a new SSH connection to Athena via the **Remote - SSH extension in VSCode** (not your operating system's terminal).
    * For `ssh user@hostname`, you will use `ssh kerberos@athena.dialup.mit.edu` with your kerberos ID.
    * You should be prompted for your kerberos password and two-factor authentification in the VSCode search bar.
    * Once successfully connected, you should be able to open your `web_scripts` folder in VSCode.
    * Within that folder, you should see the `index.html` file that was created in the last part of **Step #3**. Editing the `index.html` file will change what you see when you visit your scripts.mit.edu homepage (visit at https://kerberos.scripts.mit.edu). Note that updates may take a few minutes to appear on the web.<br><br>

7. Make a copy of of this Github repository on both your local machine and in your Athena `web_scripts` folder.
    * There are multiple ways to [transfer files between your local machine and Athena](http://kb.mit.edu/confluence/pages/viewpage.action?pageId=3907182). One simple way is with the `rsync` command in your local terminal:
        ```
        $ rsync -rav jspsych_tutorial_960 kerberos@athena.dialup.mit.edu:~/web_scripts
        ```
    * This command will copy the directory `jspsych_tutorial_960` and place it in your `web_scripts` directory on Athena.
    * A better way to keep file synchronized between a local and remote machine is with Github. If you are familiar with [setting up SSH keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh#platform-all), it is recommended you simply `git clone` this repository locally and in your Athena `web_scripts` directory.<br><br>

8. Once you have made the directory `~/web_scripts/jspsych_tutorial_960` on Athena, it should be accessible from the web. You can visit it at [https://msaddler.scripts.mit.edu/jspsych_tutorial_960](https://msaddler.scripts.mit.edu/jspsych_tutorial_960) (replace my kerberos with your own and check that it looks the same).

<br>

# Helpful resources:
- [Documentation for jsPsych](https://www.jspsych.org/) (**most helpful resource for actually coding your experiment webpage**)
    - [jsPsych tutorials](https://www.jspsych.org/7.3/tutorials/rt-task/)
    - [Overview of plugins in jsPsych](https://www.jspsych.org/7.3/overview/plugins/)
    - [Storing and manipulating data in jsPsych](https://www.jspsych.org/7.3/overview/data/) 
- [Documentation for scripts.mit.edu](https://scripts.mit.edu/web/) (particularly helpful [FAQs](https://scripts.mit.edu/faq/))
- [Brief documentation for using Athena to host a website](https://sipb.mit.edu/doc/using-athena/)
- [Kaggle](https://www.kaggle.com/datasets), a great place to find and download image datasets for machine learning
- [Hugging Face](https://huggingface.co/datasets), another great place to find and download image datasets for machine learning
    - Example images in this repository were taken from [https://huggingface.co/datasets/poolrf2001/FaceMask/tree/main](https://huggingface.co/datasets/poolrf2001/FaceMask/tree/main)
