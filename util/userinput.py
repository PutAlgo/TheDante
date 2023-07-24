import Urlsnatcher as url_class
import pdfmaker as pdfm
import danteai as gpt

def prompt_user():
    user_data = {}
    user_data['tick'] = input("Inset lowercase ticker:")
    print()
    user_data['form'] = input("What doc type?: 1.10k 2.10q. 3.both please enter by number:")

    print()
    print("Enter a year range( Ex. year1 through year2):")
    while True:
        try:
            user_data['range'] = input("Enter year1: ")[2:], input("Enter year2: ")[2:]
            break
        except:
            print('Please enter in 4 digit format')




    urls = url_class.get_url(user_data['tick'], user_data['form'], user_data['range'])
    print("gathering docs..")
    print()
    names = pdfm.make_pdf(urls,user_data)
    print("Starting nlp")
    for name in names:
        print(name)
        gpt.gpt_doc(name,user_data)


prompt_user()