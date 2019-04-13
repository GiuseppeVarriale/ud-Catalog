# Catalogls

## Overview

This is the fourth Back-end developer Udacity nanodegree project.  
The project is a catalog app, with some json end points.  
Authentication is provided by Facebook using OAuth  
Items are classified by categories.  
You can create, edit and delete your own Items when you is logged.

## Setup Project

Install VirtualBox and Vagrant:

1. Download Virtualbox [**Here**](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
2. Download Vagrant [**Here**](https://www.vagrantup.com/downloads.html)

3. If you **is** a back-end developer nanodegree student, you can Download the Vagrant File with the configurations in [**This Link**](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)\
If **not** Download or Clone [**this repository**](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile)


## Launching the Virtual Machine

1. Launch the Vagrant VM inside Vagrant sub-directory in the downloaded fullstack-nanodegree-vm repository using command:
     >`$ vagrant up`

2. Then Log into this using command:
      > `$ vagrant ssh`

3. Change directory to /vagrant and look around with ls.

## Setting up the enviroment

1. Download the content of this current repository, by either downloading or cloning it from [**Here**](https://github.com/GiuseppeVarriale/ud-Catalog.git)

2. If you cloned the content skip next step, jump to Setting up the database.

3. If Download the content manualy from github you need to move the folder to vm vagrant folder.  

## Facebook id with OAUTH

To authentication the app use facebook api with OAUTH. You need to configure it with you app_id and app_secret
More infomation about it [**here**](https://www.udacity.com/course/authentication-authorization-oauth--ud330)  

1. Configure the app_id and app_secret on file fb_create_secrets.json and on
   /templates/login.html,  
   this is provide ou your developer facebook when you  configure the facebook api [**Here**](https://developers.facebook.com/apps).  
   You can make your changes on file fb_client_secrets.json.example and save as fb_client_secrest.json

```json
file: fb_create_secrets.json

{
  "web": {  
    "app_id": "YOUR_APP_ID_HERE",  
    "app_secret": "YOUR_APP_SECRET_HERE"  
  }  
}
```

## Setting up the database

1. Access the repository folder inside the vagrant folder.

2. run the database_setup.py using command:
    > `$ python database_setup.py`

## Populating Categories

The categorias are created on createCategories.py, we used shoes categories to make this project, but  
if you want, you can edit this file and change de categories editing the file!  
on Line 21. 

```python
# createCategories.py
categories = ("Women's Shoes", "Men's Shoes", "Casual Shoes",  
              "Dress Shoes", "Boots", "Canvas Shoes")
```

> [!CAUTION]
> don't run  createCategories.py, if you want to populate with fake item to test app.

1. If you want populate only the categories run the file createCategories.py, if you want populate categories and fake items for test **don't run**  createCategories.py, **jump** to step 2.
    > `$ python createCategories.py`

2. If you want create some cateogories and items for test the app, run the file lotofthingdb.py
    > `$ python lotofthingsdb.py`

## Running the the program

- From the vagrant directory inside the virtual machine, go the repository directory and run the program  using:
     > `$ python application.py`

## Acessing the app

- Open your Web Navigator and open the url [**http://localhost:5000**](http://localhost:5000)
