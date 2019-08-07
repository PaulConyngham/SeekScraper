import xlsxwriter
url = "https://www.seek.com.au/"#Data-Scientist-jobs/in-Sydney"
search = "https://chalice-search-api.cloud.seek.com.au/search"
job = "https://www.seek.com.au/job/"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': 'application/json'
}

month = {
    '01': 'Jan',
    '02': 'Feb',
    '03': 'Mar',
    '04': 'Apr',
    '05': 'May',
    '06': 'Jun',
    '07': 'Jul',
    '08': 'Aug',
    '09': 'Sep',
    '10': 'Oct',
    '11': 'Nov',
    '12': 'Dec'
}

workbook = xlsxwriter.Workbook("Jobs.xlsx")
worksheet = workbook.add_worksheet()
row = 1
worksheet.write_row("A1", ['Title', 'Comp. Name', 'Date', 'Area', 'Work type', 'Rating', 'Apply'])