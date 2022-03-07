from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime
import math
from PIL import Image, ImageTk
import tkinter

GUI = Tk()
GUI.title('โปรแกรมจัดการไข่ฟัก')
GUI.geometry('1000x800')


### Setting Tab ###
Tab = ttk.Notebook(GUI)
Tab.pack(fill = BOTH,expand = 1)

T1 = Frame(Tab)
T2 = Frame(Tab)

# Create a photoimage object of the image in the path
image1 = Image.open('C:/Users/Rob Noiin/Desktop/Python/GUI2022/Project/egg.png')
test = ImageTk.PhotoImage(image1)

T1 = tkinter.Label(image=test)
T1.image = test

# Position image
T1.place(x= 80, y= 0)


icon_tab1 = PhotoImage(file = 'Document-icon.png')
icon_tab2 = PhotoImage(file = 'Calculator-icon.png')

Tab.add(T1, text = 'แนะนำ',image = icon_tab1,compound = 'left')
Tab.add(T2, text = 'คำนวณ',image = icon_tab2,compound = 'left')

#############zone left###########################################
RF1 = Frame(T2)#received frame 1

RF1.place(x = 50,y = 60)

BF2 = Frame(T2)#button fram 2
BF2.place(x = 150, y = 300)


LLC = Label(T2,text = 'Lab Code :',font = (None,13))#lab code 
LLC.configure(foreground="blue")
LLC.place(x = 50, y = 20)

v_labcode = StringVar()

LC = Label(T2,textvariable=v_labcode,font=(None,13))#generate lab code
LC.place(x =150 ,y = 20)
v_labcode.set('CK-1001')

def ET(GUI,text,font=('Angsana New',20)):#entry+text
	v_strvar = StringVar()
	T = Label(RF1,text = text,font = (None ,15)).pack()
	E = ttk.Entry(RF1,textvariable = v_strvar,font = font)
	return (E,T,v_strvar)

EF,L,v_farm = ET(RF1,'ชื่อฟาร์ม')#entry farm
EF.pack()

EN,L,v_quantity = ET(RF1,'จำนวนตัวอย่าง')#entry number of sample
EN.pack()

ES,L,v_status = ET(RF1,'สถานะตัวอย่าง')#entry status
ES.pack()


def writetocsv(data,filename = 'customer.csv'):
	with open(filename,'a', newline = '',encoding = 'utf-8') as file:
		fw = csv.writer(file) # file writer
		fw.writerow(data)

def writetocsv(data,filename = 'total_eggs.csv'):
	with open(filename,'a', newline = '',encoding = 'utf-8') as file:
		fw = csv.writer(file) # file writer
		fw.writerow(data)

def UpdateCSV(data,filename = 'customer.csv'):
	#data = [[a,b],[a,d]]
	with open(filename,'w',newline = '',encoding='utf-8') as file:
		fw = csv.writer(file)
		fw.writerows(data) # = replace with list

last_customer = ''
allcustomer = {}
egg = {}
total = 0
sumtotal = 0


def UpdateTable_customer():
	global last_customer
	global allcustomer
	global sumtotal
	try:
		with open('customer.csv',newline = '',encoding='utf-8') as file:
			fr = csv.reader(file)
			table_customer.delete(*table_customer.get_children())
			for row in fr:
				table_customer.insert('',0,value = row)
				labcode = row[0]
				total = row[5]
		sumtotal = row[5]
		last_customer = row[0]	
		next_customer = int(last_customer.split('-')[1]) + 1
		v_labcode.set('CK-{}'.format(next_customer))
	except:
		pass



def SaveCustomer():
	global quantity
	global total
	stampnow = datetime.now().strftime('%Y-%m-%d')
	try:
		with open('customer.csv',newline = '',encoding='utf-8') as file:
			fr = csv.reader(file)
			table_customer.delete(*table_customer.get_children())
			for row in fr:
				table_customer.insert('',0,value = row)
				stamp = row[1]
		stamp = stamp.split(' ')[0]
	except:
		stamp = datetime.now().strftime('%Y-%m-%d')
	if stampnow == stamp:
		labcode = v_labcode.get()
		stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
		farm = v_farm.get()
		quantity = v_quantity.get()
		status = v_status.get()
		total = int(sumtotal) + int(quantity) 
		writetocsv([labcode, stamp,farm, quantity,status,total],'customer.csv')
		table_customer.insert('',0,value = [labcode,stamp,farm,quantity,status,total])
		UpdateTable_customer()
		v_farm.set('')
		v_quantity.set('')
		v_status.set('ปกติ')
	else:
		total = 0
		labcode = v_labcode.get()
		stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
		farm = v_farm.get()
		quantity = v_quantity.get()
		status = v_status.get()
		total += int(quantity) 
		writetocsv([labcode, stamp,farm, quantity,status,total],'customer.csv')
		table_customer.insert('',0,value = [labcode,stamp,farm,quantity,status,total])
		UpdateTable_customer()
		v_farm.set('')
		v_quantity.set('')
		v_status.set('ปกติ')
	
def UpdateEgg():
	try:
		with open('total_eggs.csv',newline = '',encoding='utf-8') as file:
			fr = csv.reader(file)
			for row in fr:
				eggs = row[0]
		v_totalegg.set(eggs)
	except:
		pass

def Clear():
	UpdateCSV('',filename = 'total_eggs.csv')
	v_totalegg.set(0)
	v_sample.set(0)


def Calutate():
	global total_eggs
	global control_eggs
	global sample_eggs 
	global repeat_eggs
	global now_eggs
	global now_sample
	stampnow = datetime.now().strftime('%Y-%m-%d')
	with open('customer.csv',newline = '',encoding='utf-8') as file:
		fr = csv.reader(file)
		table_customer.delete(*table_customer.get_children())
		for row in fr:
			table_customer.insert('',0,value = row)
			stamp = row[1]
			total = row[5]
	last_stamp = stamp.split(' ')[0]
	total = row[5]
	if stampnow == last_stamp:
		total_eggs = int(v_totalegg.get())
		if total_eggs%2 != 0:
			total_eggs = total_eggs - 1
		control_eggs = 6
		sample_eggs = int(total)*2
		repeat_eggs = int(round(int(total)*0.1,0))*2
		now_eggs = total_eggs - control_eggs - sample_eggs - repeat_eggs
		now_sample = (now_eggs/2) - int(math.ceil(float(now_eggs)*0.1))/2
	elif stampnow != last_stamp and sumtotal == total:
		total = quantity
		total_eggs = int(v_totalegg.get())
		if total_eggs%2 != 0:
			total_eggs = total_eggs - 1
		control_eggs = 6
		sample_eggs = int(total)*2
		repeat_eggs = int(round(int(total)*0.1,0))*2
		now_eggs = total_eggs - control_eggs - sample_eggs - repeat_eggs
		now_sample = (now_eggs/2) - int(math.ceil(float(now_eggs)*0.1))/2
	else:
		total = sumtotal
		total_eggs = int(v_totalegg.get())
		if total_eggs%2 != 0:
			total_eggs = total_eggs - 1
		control_eggs = 6
		sample_eggs = int(total)*2
		repeat_eggs = int(round(int(total)*0.1,0))*2
		now_eggs = total_eggs - control_eggs - sample_eggs - repeat_eggs
		now_sample = (now_eggs/2) - int(math.ceil(float(now_eggs)*0.1))/2
	v_sample.set(int(now_sample))
	eggs = total_eggs
	writetocsv([eggs],'total_eggs.csv')
	return total_eggs, control_eggs,sample_eggs,repeat_eggs,now_eggs,now_sample
	

def SummaryWindow(event = None):#ต้องใส่เมี่อต้องการกดปุ่ม
	
	class Table:
	    def __init__(self,Sum):
	         
	        # code for creating table
	        for i in range(total_rows):
	            for j in range(total_columns):
	                 
	                self.e = Entry(Sum, width=20, fg='blue',
	                               font=('Arial',16,'bold'))
	                 
	                self.e.grid(row=i, column=j)
	                self.e.insert(END, lst[i][j])
	 
	# take the data
	Calutate()
	lst = [('ไข่ฟักทั้งหมด',total_eggs,'ฟอง'),
	       ('ไข่ฟักตัวควบคุม',control_eggs,'ฟอง'),
	       ('ไข่ฟักตัวอย่าง ',sample_eggs,'ฟอง'),
	       ('ไข่ฟักสุ่ม 10%',repeat_eggs,'ฟอง'),
	       ('ไข่ฟักคงเหลือ',now_eggs,'ฟอง')]
	  
	# find total number of rows and
	# columns in list
	total_rows = len(lst)
	total_columns = len(lst[0])
	  
	# create root window
	Sum = Tk()
	t = Table(Sum)
	Sum.mainloop()


	


BSave = ttk.Button(BF2, text = 'SAVE',command = SaveCustomer)
BSave.grid(row = 0, column = 0,ipadx = 20,ipady = 10,pady = 5)


TF3 = Frame(T2)#table frame 3
TF3.place(x = 400 ,y = 80)

header = ['Lab Code','Date time','Farm','Quantity','Status','Total']
hwidth = [70,120,100,80,80,80] # pixel

L = Label(T2,text = '                                  History table                                   ',font = ('Angsana New',15))
L.place(x = 400, y = 50)
L.config(bg="yellow")

table_customer = ttk.Treeview(TF3,columns = header, show = 'headings',height= 10)
table_customer.pack()

for hd in header:
	table_customer.heading(hd, text = hd)

for hd,hw in zip(header,hwidth):
	table_customer.column(hd,width = hw)

SF4 = Frame(T2)#summary fram 4
SF4.place(x = 400, y = 400)

BSF5 = Frame(T2)#button summary fram 5
BSF5.place(x = 500, y = 510)

v_totalegg = StringVar()
LTotal = ttk.Label(SF4, text = 'ไข่ฟักทั้งหมด',font = ('Angsana New',14))
LTotal.grid(row = 0, column = 0)
ETotal = ttk.Entry(SF4, textvariable = v_totalegg,font = ('Angsana New',14) )
ETotal.grid(row = 0, column = 1)
L = ttk.Label(SF4, text = 'ฟอง',font = ('Angsana New',14))
L.grid(row = 0, column = 2)


v_sample = StringVar()
L = ttk.Label(SF4, text = 'จำนวนตัวอย่างที่สามารถตรวจได้',font = ('Angsana New',14))
L.grid(row = 1, column = 0,pady = 10)
L = ttk.Label(SF4, textvariable = v_sample,font = ('Angsana New',14))
L.grid(row = 1, column = 1,pady = 10)
L = ttk.Label(SF4, text = 'ตัวอย่าง',font = ('Angsana New',14))
L.grid(row = 1, column = 2,pady = 10)

BCal = ttk.Button(BSF5, text = 'Calulate',command = Calutate)
BCal.grid(row = 3, column = 0,ipadx = 20,ipady = 10,padx = 5)

BShow = ttk.Button(BSF5, text = 'Show',command = SummaryWindow)
BShow.grid(row = 3, column = 1,ipadx = 20,ipady = 10,padx = 5)

BClear = ttk.Button(BSF5, text = 'Clear',command = Clear)
BClear.grid(row = 3, column = 2,ipadx = 20,ipady = 10,padx = 5)





UpdateEgg()
UpdateTable_customer()
GUI.mainloop()