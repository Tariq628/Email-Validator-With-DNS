
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import re
import requests
from validate_email import validate_email,  validate_email_or_fail

# Create your views here.
def index(request):
    return render(request, "index.html")


regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
def isValid(email):
    if re.fullmatch(regex, email):
      print("Valid email")
      return "Valid! "
    else:
      print("Invalid email")
      return "Invalid! "


@csrf_exempt
def return_csv(request):
    print(request.FILES)
    post_text = request.FILES.get('the_post')
    try:
        with open('csv_file.csv', 'w', newline='') as f:
            for line in post_text:
                # create the csv writer
                writer = csv.writer(f)

                # write a row to the csv file
                writer.writerow(line.decode().replace('\r\n', '').split(","))
    except Exception as e:
        if hasattr(e, 'message'):
            print("Hi", e)
            return JsonResponse({'message': e.message}, safe=False)
        else:
            return JsonResponse({'message': "Something Went Wrong"}, safe=False)


    my_arr = []
    def add_col_to_csv(csvfile,fileout):
        try:
            with open(csvfile, 'r') as read_f, \
                open(fileout, 'w', newline='') as write_f:
                csv_reader = csv.reader(read_f)
                csv_writer = csv.writer(write_f)
                for index, row in enumerate(csv_reader):
                    print(row)
                    if index == 0:
                        for row_index, item in enumerate(row):
                            if item.lower() == 'email':
                                email_coulmn_no = row_index
                                break
                            else:
                                email_coulmn_no = 1

                    if index != 0:
                        if index > 10:
                            break
                        try:
                            # status = validate_email(row[email_coulmn_no], verify=True)
                            email = row[email_coulmn_no]
                            status = isValid(email)
                            if status == "Valid! ":
                                status = validate_email_or_fail(email_address=row[email_coulmn_no])
                            print("status", status)
                        except Exception as e:
                            status = e.__class__.__name__
                    else:
                        status = 'Status'
                    my_arr.append(f'The status of {row[email_coulmn_no]} is {status}')
                    row.append(status)
                    csv_writer.writerow(row)
        except Exception as e:
            if hasattr(e, 'message'):
                return JsonResponse({'message': e.message}, safe=False)
            else:
                return JsonResponse({'message': "Something Went Wrong"}, safe=False)

    add_col_to_csv('csv_file.csv','static/media/updated_file.csv')
    return JsonResponse({'message': 'File updated! ', 'my_arr':my_arr}, safe=False)


