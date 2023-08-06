# How to label the data for supervised learning
For supervised learning you may often need a csv file with the
filenames and labels. Just look at the following example.

You have a folder with files: 

<img src="label/images/data.PNG" alt="Your data">

You want a csv file like that: 

<img src="label/images/csv.PNG" alt="Csv file">

Take the following steps: 

    pip install label

If you haven't already installed pandas and glob, also run:

    pip install pandas glob3

and if you use python2:

    pip install pandas glob2

You can then start the python interpreter from the terminal typing:

    python

Then within the Python interpreter, you can use the label package:

    from label import create_csv

and start the step-by-step instruction typing:

    create_csv()

<img src="label/images/scr1.PNG" alt="Screenshot 1"> <br/>

<img src="label/images/scr2.PNG" alt="Screenshot 2"> <br/>

<img src="label/images/scr3.PNG" alt="Screenshot 3"> <br/>

<img src="label/images/scr4.PNG" alt="Screenshot 4"> <br/>

<img src="label/images/scr5.PNG" alt="Screenshot 5"> <br/>

<img src="label/images/scr6.PNG" alt="Screenshot 6"> <br/>
    
