
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import re
# from email_validator import validate_email, EmailNotValidError
# from pyisemail import is_email
from validate_email import  validate_email_or_fail
# from verify_email import verify_email

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
                                print("esle")
                                email_coulmn_no = 1
                            
                    if index != 0:
                        # bool_result_with_dns = is_email(row[email_coulmn_no], check_dns=True)
                        # detailed_result_with_dns = is_email(row[email_coulmn_no], check_dns=True, diagnose=True)
                        # status = isValid(row[email_coulmn_no])
                        # status = is_email(row[email_coulmn_no], check_dns=True, diagnose=True)
                        # if index > 50:
                        #     break
                        try:
                            # status = validate_email(row[email_coulmn_no], verify=True)
                            status = validate_email_or_fail(email_address=row[email_coulmn_no])
                            # status = verify_email(row[email_coulmn_no], debug=True)
                        except Exception as e:
                            print(e)
                            status = e.__class__.__name__
                    else:
                        status = 'Status'
                    print(index, row[email_coulmn_no])
                    row.append(status)
                    csv_writer.writerow(row)
        except Exception as e:
            if hasattr(e, 'message'):
                return JsonResponse({'message': e.message}, safe=False)
            else:
                return JsonResponse({'message': "Something Went Wrong"}, safe=False)
    add_col_to_csv('csv_file.csv','static/media/updated_file.csv')

    return JsonResponse({'message': 'File updated! '}, safe=False)


