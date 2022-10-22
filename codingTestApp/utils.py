import re
from openpyxl import load_workbook


def validate_email(email):
    """
    Desc: Validate email.
    Parameters: email[str]
    Return: bool
    """
    #use regurlar expression to check valid email
    #Example: https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    if email is None: return False

    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)): return True
    else: return False



def validate_phone_number(phone_number):
    phone_ = str(phone_number)
    if (len(phone_) != 9): return False
    if not ( phone_.startswith('78') or phone_.startswith('79') or phone_.startswith('73')): return False
    return True

def validate_NID(nid):
    """
    Desc: Validate National Identity Card.
    Parameters: String
    Return: Boolean
    """

    
    #[STEP> Call NIDA for validation]
    return (len(str(nid)) == 16)



def getDataFromExcel(excel_file):
    """
    Extract data from excel file
    Return list of dict
    """

    index = 0
    workbook = load_workbook(filename=excel_file)
    sheet =  workbook.active
    
    data = list()

    for row in sheet.rows:
        if (index == 0):
            index += 1
            continue
        data.append(
            {
                'names': row[0].value,
                'nid': int(row[1].value),
                'phone_number': int(row[2].value),
                'gender': row[3].value,
                'email': row[4].value
            }
        )
        print('NID:', int(row[1].value))
    return data

def validate_data(data):
    """
    """
    validated_data = list()
    
    for item in data:
        item['phone_valid'] = validate_phone_number(item.get('phone_number'))
        item['nid_valid'] = validate_NID(item.get('nid'))
        item['email_valid'] =  validate_email(item.get('email'))
        validated_data.append(item)

    return validated_data