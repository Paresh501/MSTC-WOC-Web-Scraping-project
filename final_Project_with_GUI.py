from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import requests
from tkinter import *
from tkinter import ttk


root = Tk()
root.state('zoomed')

photo = PhotoImage(file="CLG.png")
background_label = Label(root, image=photo)
background_label.place(x=0, y=0)
background_label.image = photo

cityvar=StringVar()
city=None
lbl=Label(root, text=" Enter city/state to find colleges : ", pady=15, font=('Times',20, 'bold'), fg="red", bg='aliceblue').pack()
x=Entry(root, textvariable=cityvar, width=40).pack()
def get_detail(stream):
    global city
    city=cityvar.get()
    city=city.lower()

    for i in tree.get_children():
            tree.delete(i)
    
    #finding stream

    if stream=='b-tech':
        link='https://www.shiksha.com/b-tech/colleges/b-tech-colleges-'
    if stream=='mba':
        link='https://www.shiksha.com/mba/colleges/mba-colleges-'
    if stream=='law':
        link='https://www.shiksha.com/law/colleges/colleges-'
    if stream=='design':
        link='https://www.shiksha.com/design/colleges/colleges-'


    #finding page_no

    r=requests.get(link+city, headers={'User-Agent': 'Mozilla/5.0'})
    html=r.content
    soup=BeautifulSoup(html,"html.parser")
    page_no=[]
    page=soup.find("div", {"class":"pagnation-col"})
    if (page==None):
        page_no.append(1)
    else:
        for i in page.findAll('a'):
            x=i.text
            if (x!="  "):
                page_no.append(x)
    
    
    for Q in range(len(page_no),0,-1):

        k=(Q-1)*20
        
        #scraping Data from Shiksha.com
        print(Q)
        r=requests.get(link+city+'-'+str(Q), headers={'User-Agent': 'Mozilla/5.0'})
        html=r.content
        soup=BeautifulSoup(html,"html.parser")
        table=soup.find("table", {"cellpadding":"0"})
        print(Q)

        #finding clg name using RegEx

        name=re.compile(r'<td>[A-z/ -;]*</td>')
        clg_nametemp=[]

        for i in re.findall(name, str(table)):
            clg_nametemp.append(i)
    
        clg_name=[]
        j=0
    
        for i in clg_nametemp:
            x=re.sub('<td>', '', clg_nametemp[j])
            x=re.sub('</td>', '', x)
            if (j%3==0):
                clg_name.append(x)
            j+=1
    


        #finding clg Address using RegEx

        add_pattern=soup.findAll("p", {"class":"ctp-cty"})
        clg_add=[]
        for i in soup.findAll("p", {"class":"ctp-cty"}):
            clg_add.append(i.text)
        

        #finding clg Fees using RegEx

        fee_pattern=re.compile(r'<td>[A-z/ -;]*</td>')
        clg_fee_temp=[]

        for i in re.findall(fee_pattern, str(table)):
            clg_fee_temp.append(i)
    
        clg_fee=[]
        j=0
    
        for i in clg_fee_temp:
            x=re.sub('<td>', '', clg_fee_temp[j])
            x=re.sub('</td>', '', x)
            if ((j+1)%3==0):
                clg_fee.append(x)
            j+=1


        #finding facility provided by clg using RegEx

        clg_link=[]
        for i in soup.findAll("div", {"class":"ctpSrp-Lft"}):
            link1=i.find('a')
            x=link1.get('href')
            clg_link.append(x)
        clg_facility=[]
        clg_rating=[]

        for i in clg_link:
            r1=requests.get(i, headers={'User-Agent': 'Mozilla/5.0'})
            html1=r1.content
            soup1=BeautifulSoup(html1,"html.parser")
            f=soup1.find("ul", {"class":"infra flex-ul"})
            f_pattern=re.compile(r'<p>([A-z|/|-]*)')
            faci=re.findall(f_pattern, str(f))
            clg_facility.append(faci)

            #finding rating of clg using RegEx
            

            r=soup1.find("div", {"class":"location-of-clg"})
            rating_pattern=re.compile(r'<span class=.rating-block.>\n.....')
            temp=re.findall(rating_pattern, str(r))
            if (len(temp)==0):
                temp1='-'
            else:
                temp1=temp[0]
                temp1=re.sub('^<span class=.rating-block.>\n..', '', temp1)
            clg_rating.append(temp1)

        

        j=0
        for i in clg_name:
            k+=1
            if (j%2==0):
                tree.insert("", j, text=str(k)+'. '+i, values=(clg_add[j], clg_fee[0], clg_facility[j], clg_rating[j]), tags=('x'))
            else:
                tree.insert("", j, text=str(k)+'. '+i, values=(clg_add[j], clg_fee[0], clg_facility[j], clg_rating[j]), tags=('y'))
            j+=1



btn1=Button(root, text="Find Engineering colleges", command=lambda: get_detail('b-tech'), fg='red', bg='lightyellow').pack(pady=5)
btn2=Button(root, text="Find MBA/PGDM colleges", command=lambda: get_detail('mba'), fg='red', bg='lightyellow').pack(pady=5)
btn3=Button(root, text="Find Law colleges", command=lambda: get_detail('law'), fg='red', bg='lightyellow').pack(pady=5)
btn4=Button(root, text="Find Design colleges", command=lambda: get_detail('design'), fg='red', bg='lightyellow').pack(pady=5)  #submit btn

root.title("Get College Details by Entering location")

tree = ttk.Treeview(root)

tree["columns"]=("adress", "fees", "facility", "rating")
tree.column("#0",width=350)
tree.column("adress", width=80)
tree.column("fees", width=20)
tree.column("facility", width=315)
tree.column("rating", width=1)

tree.heading("#0", text="College name",anchor="w")
tree.heading("adress", text="Address",anchor="w")
tree.heading("fees", text="Fee",anchor="w")
tree.heading("facility", text="Facility",anchor="w")
tree.heading("rating", text="Rating",anchor="w")

style = ttk.Style(root)

# setting ttk theme to "clam" which support the fieldbackground option

style.theme_use("clam")
style.configure("Treeview", background="lightyellow", 
                fieldbackground="lightyellow", foreground="white")

tree.tag_configure('x', background='lightgrey', foreground='black', font=('Arial',10))
tree.tag_configure('y', background='lightyellow', foreground='black', font=('Arial',10))
s = ttk.Style()
s.configure('Treeview', rowheight=25)
style.configure("Treeview.Heading", font=('Arial', 11))

tree.pack(side=TOP, fill='both', expand=1)

root.mainloop()
