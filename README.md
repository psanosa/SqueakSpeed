# SqueakSpeed
Source code and pipeline analysis for the wheel tracking system.
1. Hardware Installation 
2. Open-source code for the live tracker written in Python
3. Live-tracker setup 
4. Analysis pipeline written in R (Optional)

# Hardware Installation Instruction
**List of Materials:**

Raspberry Pi (Any model that has Wi-Fi or Ethernet connectivity)

Micro SD Card (to install Operating System)

Micro SD Card Adapter 

Breadboard (If you are running multiple cages) 

Breadboard power supply module (If you are running multiple cages) 

Jumper Wires

Hall Sensor (Unipolar)

Neodymium magnets


1. Setup your Raspberry Pi with downloading the latest version of RasPi OS using Raspberry Pi Imager on the Raspberry Pi main website. Go through the Raspberry Pi Imager software on your own personal laptop or desktop computer. Go through the steps it asks to set up the operating system for you. You will need a micro SD card adapter to plug into your own personal laptop or desktop computer to download the OS into the micro SD card. (**The model and diagram that I will be showcasing is for the Raspberry Pi Model 4B**)
2. Setup the breadboard power supply module along with the breadboard. (**skip this step if you are running only a single cage**)
4. Choose whether you are running multiple sensors simultaenously or just one. Regardless, it is a good thing to note that 3 pins exist for the hall sensor: a digital output (DO), VCC (voltage supply), and ground. The order in which this appears will differ on the small circuit board I have used compared to using only the hall sensor itself (no LED indicator). I have included both diagrams on this repository. **If using only a single hall sensor skip this step and move on to step 4.** When using multiple sensors simultaenously (therefore running multiple cages), make sure to setup the wiring diagram as seen here. It is important to note that the VCC pins of each sensor should not be directly supplied from the Raspberry Pi as this will cause the computer to short circuit. Also, make sure the breadboard's ground is linked with the Raspberry Pi's ground pin. 
5. If using a single hall sensor, the hall sensor pins can directly connect to the Rasperry Pi. First, connect the DO pin to any DO pin in the Raspberry Pi (**indicated by the pins of the Raspberry Pi; GPIO.png. The eligible pins to use are the ones with just GPIO then a number coming right after it, e.g. GPIO 27**). Second, connect the ground pin of the hall sensor to any ground pin on the Raspberry Pi. When connecting the VCC pin of the hall sensor, it is advisable to not use the 5.5 V pin that the Raspberry Pi supplies as this may cause a short circuit. Instead, use the 3.3 V pin.
6. Assuming that you are using a hall sensor that is integrated on a board with LEDs. To test if the hardware is functional around the hall sensor, simply place a magnet in proximity of the sensor. The LED that is off should light up. If you are simply using the hall sensor by itself, testing for hardware functionality is included in the category below (in steps **14** and **15**). 

**NOTE:** The magnetic polarities between the sensor and the magnet (e.g north and south poles). To check, the back of the hall sensor should be the flat side and the front should be the one that's not flat. If you place the magnet in proximity of the back and the inactivated LED lights up, you are dealing with the south pole end from the hall sensor that attracts the north pole end of the magnet. If you place the magnet in proximity of the front and inactivated LED lights up, then you are dealing with the north pole end from the hall sensor that attracts the south pole end of the magnet. This will matter when and how you place the magnet on your own voluntary wheel setup.

# Source Code Installation and Live-Tracking Setup Instructions 
1. Create an account on ThingSpeak.com.
2. Go to Channels > My Channels > New Channel. 
3. Add in the name tag and description of the rodent.
4. In order to make sure that live data is visible, it is **IMPORTANT** to only check 4 fields and add in the parameters of interest in this order: **Field 1 = Rotations**, **Field 2 = Distance**, **Field 3 = Speed**, and **Field 4 = Acceleration**. Once done, save the changes to your channel. 
5. Go to Devices > MQTT. Add in the name and description. Under the "Authorize channels to access", select the channel previously created then click on add the channel and tick the "Allow Publish" and "Allow Subscribe" boxes. 
6. You should now receive your **MQTT Credentials**. Make sure to download your credentials and store this in a safe location (**make backups**). These credentials are needed in the source code.
7. Along with your MQTT Credentials, make sure to also note the **Write API Key** and **Channel ID** as these will be used in the source code.
8. The steps followed from 1-8 are for a **single channel** or rodent to record. If you are **recording multiple rodents**, repeat steps 1-8 until the desired number (with a maximum of 6) channels are achieved.

Now it's time to put these values onto the source code.

9. Download the .py file in this repository and open it in **Thonny** through the Raspberry Pi.
10. Open the **terminal** on the Raspberry Pi, type to install this package: **pip3 install paho.mqtt** (If you get “externally-managed-environment” on newer Raspberry Pi OS versions, use **pip3 install schedule --break-system-packages**)
11. Open the **terminal** on the Raspberry Pi, type to install this package: **pip3 install schedule** (If you get “externally-managed-environment” on newer Raspberry Pi OS versions, use **pip3 install paho.mqtt --break-system-packages**)
12. Now go back to Thonny and change the wheel diameter variable (**in meters**) to the specific wheel you are using. For instance, wheeldiameter = 0.303
13. Under "# MQTT credentials for the device, # The ThingSpeak Channel ID, and # The Write API Key for the channel" within the code, write the respective values that was previously recorded in Steps 7 and 8. Save the code.
14. To test for software functionality, run the code and simply wait a minute for a value of 0 to get plotted on the ThingSpeak channel. 
15. To test for software and hardware functionality, wave the magnet across the hall sensor a couple of times, then wait a minute until a recorded value shows up on the channel that you have made.
    

# Data Conversion and Analysis Instructions (Optional)
This pipeline analysis is used to get the average, total, SD, and SEM of a parameter per hour. This organizes the data for the input into PRISM. 
1. Download the latest version of RStudio. 
2. Once satisfied with the experiment, export the files from their respective ThingSpeak channels as a .csv file. (**NOTE:** the files downloaded as a .csv gets a default name, so ensure to immediately change the file name to the ID of the rodent once downloaded to differentiate between the different channels' data).
3. The .csv file should now be available to be imported with its proper file name into RStudio.
4. Download the .R analysis script in this repository.
5. Create a new folder on the desktop and put all the downloaded .csv of the channels in it.
6. Open RStudio and select New Project > Existing Directory and select the folder that has all the .csv files.
7. Right-click and import the data set of the first rodent ID to the global environment.
8. Open the .R analysis script in this RStudio project. 
9. Where it says "read.csv(___)" on the script, **MAKE SURE** to input the correct file name. It will be difficult to track the data of the file that has been mistakenly copied from the initial rodent ID to one of the other rodent IDs, if there are multiple. 
10. There are going to be 4 parameters that you need to edit on the script to get the proper result: **RotSess**, **SessDist**, **AvgSpeed**, and **AvgAcc**.
   

    average_value = mean(INPUT PARAMETER HERE),

    sum_value = sum(INPUT PARAMETER HERE),

    standard_deviation = sd(INPUT PARAMETER HERE),

    standard_error = sd(INPUT PARAMETER HERE) / sqrt(n())

    For example, if you choose to get the results from rotations, then you input RotSess in each line onto "INPUT PARAMETER HERE".

11. Once completed, make sure to name the file for the new dataset for the parameter chosen in the line "write.csv(result, file = "INPUTRODENTID_INPUTPARAMETERANALYZED.csv")".
12. You should now have a new file added to your folder. If you choose to analyze all parameters from a single rodent ID (distance, rotations, speed, acceleration), then you should have 4 new files added for a single rodent ID. 
13. The last line of the script allows you to reset the script. You can then can begin to input a different parameter for the same rodent or analyze an entirely different rodent by going back to Step 8.
