Introduction
=======
**Welcome to Habitat for Humanity Nepal's scripts for safely managing public facing OSM data and private ODK/OMK survey data in a PostGIS database. There are also some as well as some other goodies.**


How to use this
---------------
This a collection of scripts written in Python 2.7. It hasn't been tested with Python 3 and you'd probably find some bugs. At the moment all scripts are command line based or modules that you can import. 


General thoughts
---------------
The scripts were made with HFH-Nepal requirements in mind however they can be generalized to other contexts. The plan is to one day build a user interface - so PRs are welcomed for this any other contributions ;) Feel free to get in touch if you have any questions on how to contribute or use this code. 

Setup
---------------
A virtualenv is always a good idea to have. [This is](http://docs.python-guide.org/en/latest/dev/virtualenvs/) a tutorial that always makes the most sense to me if you're looking to set one up.

    $ git clone https://github.com/eoglethorpe/hfh.git
    $ cd hfh
    $ python setup.py install
  

Modules
=======

ETL
---
This is a collection of modules that allows for merging private ODK data with public OSM data. 

It has a few assumptions...

 - Data is collected using [OpenMapKit](http://openmapkit.org/)'s survey management server and mobile app. 
 - You are using a PostGIS database
 - In `main.py` that you are using two servers: one for hosting your OMK server and one for scripting purposes. You could certainly run these scripts on your OMK server although the code would take some modifying.
 - You are using [Amazon Web Services](aws.amazon.com) to host your servers. If you aren't, again this isn't a big issue but you would have to change around some logic of the code that transfers data between environments.



**Setup**

Before you can run the script, you have to specify some values in `config.ini` which is located in `hfh/etl/`. A blank file is contained which has the following parameters (all of which are mandatory):

    [AWS]
    PEM: location of permission key (the/path/key.pem)
    
    INIT_LOC: directory of where survey data is stored. By default: /opt/omk/OpenMapKitServer/data/
    
    INIT_IP: IP address of the server from which data is being pulled
    
    DEST_LOC: IP address of a scripting server from where the scripts are being executed
    
    [DB]
    CXN: A full connection string to the database and schema where your data will be stored
    
    HH_ID_COL: Name of your beneficiary ID column in the survey data. This can be a nested answer so make sure you include the full qualifier. For instance, if you have a section called 'General Info' and your question is labeled 'Registration Number', the value would be general_info_registration_number
    
    UID_COL: Column containing a UUID. By default this is meta_instanceId
    
    [OSM]
    WAY_COL: The prefix that of columns added to your table that contain OSM data. Default is geometry_coordinates

**What exactly does it do?**

You start by collecting mobile surveys and then uploading them to the OMK server. Once you have done this, create the necessary database schema and  execute the following found in `hfh/etl/`:
		
	python models.py
    python main.py
   
The code the does the following (with some optional manual intervention required for updating Way and Node IDs):

 1. All data is pulled from the OMK server and sent to a scripting server. 
 2. All surveys are then iterated through and each entry is read. We extract a json file consisting of survey responses and a .osm file if there was an OSM response. 
 3. A main table is created for each survey where each column consists of a response and row is a response. 
 4. The script identifies responses that are repeating or nested and creates a relational table for repeating questions.
	 - If it is a repeating response (ie attributes of individual family members), a relational table is created for each question group and responses are added.
	 - If it is nested, the values are broken up into individual columns. For instance, there are by default 5 or 6 values for ‘metadata’ which are broken up, each with their own individual column. 
 5. .osm files are also read and an XML blob is stored in a separate column. The blob is then parsed to look for the most recent way id and node id.
 - All new way IDs and node IDs are gathered and the queried to OSM via overpass. The resultset is then inserted into a given surveys main table where each response type has its own column (ie way attributes, location etc). This is where PostGIS is handy because we use POLYGON and POINT column types for ways/nodes.
 6. At this point you can manually go through your entries and make sure that the way IDs are accurate and fill in any missing Way or Node IDs for entities that are added after the fact. One way to do this is to create polygons in JOSM. 
 7. Once the new IDs have been generated and updated in the table, you execute a method that queries OSM with these new IDs and then updates the associated value for the entry's OSM data. This can be done through the following... 

In a Python shell in the `hfh/etl` directory execute the following:    

    $ import osm
    $ osm.update_all_osm(schema, survey_nm, uuidcol, wcol, ncol)
    # schema: the schema in your database where your data is
    # survey_nm: the name of the survey you would like to update
    # uuidcol: the column you are using as your UUID
    # wcol: the column that specifies way IDs
    # ncol: the column that specifies node IDs

QR Code generation
------------------
`utils/qr/qrgen.py` is a script that will create a batch of QR codes that can be used for activities like creating beneficiary cards. Its inputs are as follows:

      --path TEXT          path to CSV
      --id_col_name TEXT   column with existing unique IDs
      --vdc_col_name TEXT  column with existing VDC IDs
      --num INTEGER        how many unique IDs to generate
      --vdcs TEXT          comma delimited list of vdcs

The script works by inputting a CSV containing any existing IDs that you may have in a given geographic area (or VDC in Nepali context) and then generating a new batch of QR codes that do not overlap with current IDs.

The script will then output a new CSV containing:

    ID merge (VDC + ID) | link to QR code image | VDC | ID

Once you have completed this and if you would like to create something like beneficiary cards, you can follow [this tutorial](http://gcostudios.com/designing-and-data-merging-with-multiple-records-in-indesign-cs6/) that uses InDesign. 


