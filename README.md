# MIT 9.60 Tutorial: Online Psychophysics Experiments

## Introduction

This tutorial covers how to build an online experiment to measure human visual behavior. This tutorial covers two important components of building your first online psychophysics experiment:

1. Using a free, open-source JavaScript framework ([jsPsych](https://www.jspsych.org/7.3/)) to create behavioral experiments that run in a web browser
2. Hosting an experiment on he web via [Athena web scripts](https://scripts.mit.edu/web/)

With just these pieces, it can be quite straightforward to collect data from huge numbers of participants using crowd-sourcing platforms such as [Prolific](https://www.prolific.co) and [Amazon mTurk](https://www.mturk.com). For 9.60 projects, you will have the option to collect participants from online crowd-sourcing platforms, but it is not required. A well-designed web browser experiment will also make data collection from friends, classmates, and colleagues **much easier and faster**. The purpose of this tutorial is to show you how easy [jsPsych](https://www.jspsych.org/7.3/) makes it to build online behavioral experiments that go way beyond what is possible with simple survey platforms (i.e., Google forms). A few features of well-designed visual psychophysics experiments that are easy to implement include:
- Present stimuli for a fixed period of time
- Randomize trial order
- Collect reaction times
- Option to provide feedback on trials


## Setup

Before the tutorial, please attempt the following:
1. Install [Visual Studio Code (VSCode)](https://code.visualstudio.com/download) if you do not already have it on your local machine. It is a very convenient text editor for code that will allow you to directly edit files on a remote server (i.e., on the Athena web server where your experiment website will be hosted).

2. Within VSCode, install the [Remote - SSH](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) extension. This can be done by going to the Extensions tab > search "ms-vscode-remote.remote-ssh". This extension will enable VSCode to make an SSH connection from your local machine to the Athena web server, allowing you to directly edit files on Athena with VSCode (rather than using a command-line editor or sending files back and forth).

3. Connect to the Athena web server and enable [web scripts](https://scripts.mit.edu/web/):
    * In your local machine's terminal (not VSCode), run "`ssh kerberos@athena.dialup.mit.edu`" to initiate an SSH connection to the Athena web server (replace `kerberos` with your kerberos ID).
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
        $ echo "You have reached the mit.scripts.edu homepage of $(whoami)" > web_scripts/index.html
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

5. End your terminal's SSH connection to Athena using the `exit` command or `Ctrl-D`.<br><br>

6. Follow [these instructions](https://code.visualstudio.com/docs/remote/ssh#_connect-to-a-remote-host) to make an SSH connection to Athena using the **Remote - SSH extension in VSCode**.
    * For `ssh user@hostname`, you will use `ssh kerberos@athena.dialup.mit.edu` with your kerberos ID.
    * You should be prompted for your kerberos password and two-factor authentification in the VSCode search bar.
    * Once successfully connected, you should be able to open your `web_scripts` folder in VSCode.<br><br>

7. Make a copy of this repository in your `web_scripts` directory on Athena.
    * Easiest way:
        ```
        msaddler@department-of-alchemy:~/web_scripts$ wget https://github.mit.edu/msaddler/jspsych_tutorial_960/archive/refs/heads/main.zip
        msaddler@department-of-alchemy:~/web_scripts$ unzip main.zip
        ```
    * Better way: `git clone` this repository directly (may require setting up SSH keys and linking them to your github account.


## Key resources:
- https://www.jspsych.org/7.3/
- https://www.jspsych.org/7.0/overview/data/#storing-data-permanently-as-a-file
- http://kb.mit.edu/confluence/pages/viewpage.action?pageId=3907090
- https://scripts.mit.edu/web/
- https://huggingface.co/datasets/poolrf2001/FaceMask/blob/main/test.zip
