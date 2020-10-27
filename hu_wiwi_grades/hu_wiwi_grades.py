import pandas as pd
import numpy as np
import requests
import tabula
from bs4 import BeautifulSoup

def list_sources(url = "https://www.wiwi.hu-berlin.de/de/studium/pa/noten"):  
 """Scrapes url sources that list grading overviews of the Faculty of Economics and Business Administration of the Humboldt-Universität of Berlin.

 Parameters
 ----------
 url : str
     URL listing the current grading overview of the HU WiWi Faculty. Defaults to "https://www.wiwi.hu-berlin.de/de/studium/pa/noten".

 Returns
 -------
 dict
     containing the semesters as keys and the corresponding URLs listing grading overview as values. 
 """
 soup = BeautifulSoup(requests.get(url).content, 'lxml')
 latest = ""
 if "semester" in str(soup.find('h4')):
    semester = soup.find('h4').getText()
 elif "semester" in str(soup.find('h3')):
    semester = soup.find('h3').getText()
 else:  
    semester = "current"
 urls = {semester: url} 
 for i in soup.find_all('p'):
  if i.find("a") != None:
    a = i.find("a")
    link = a.attrs['href']
    if "resolveuid" in link:
      link = "https://www.wiwi.hu-berlin.de/de/studium/pa/" + link
    if "mailto" in link:
      continue
    if "AGNES" in a.text:
      continue
    temp = {a.text: link} 
    urls.update(temp)
 return urls

def scrape_overview(url = "https://www.wiwi.hu-berlin.de/de/studium/pa/noten", exam = ""): 
 """Scrapes the latest grading overview from the Faculty of Economics and Business Administration of the Humboldt-Universität of Berlin and returns the overview or a subset based on the entered exam specification.

 Parameters
 ----------
 url : str
     URL listing the current grading overview of the HU WiWi Faculty.
     Defaults to "https://www.wiwi.hu-berlin.de/de/studium/pa/noten".
     
 exam : str
     Exam search filter by name. 
     Defaults to "" (no search specification).
 
 Returns
 -------
 pd.DataFrame 
      Dataframe containing an exam overview. Data columns are as follows:

        ==================  ==============================================================
        exam                The exam name (as `str`)
        date_published      Date of the grading (as `str`)
        exam_review_details Details listing the review possibilities (as `str`)
        semester            The corresponding semester of the publication (as `str`)
        ==================  ==============================================================
 """
 soup = BeautifulSoup(requests.get(url).content, 'lxml')
 df = pd.DataFrame(columns = ["exam", "url", "date_published", "exam_review_details", "semester"])
 for i in soup.find_all('tbody'):
    for y in i.find_all("tr"):
     if y.find("td") == 0:
      continue
     text = y.find_all("td")
     if str(text) == "[]":
      continue
     if "strong" in str(text[0]):
      continue
     if text[0].find('a') is None:
       url = "" 
     else:
       url = text[0].find('a').attrs['href']
       if "resolveuid" in str(url):
        url = "https://www.wiwi.hu-berlin.de/de/studium/pa/" + url
     if "semester" in str(soup.find('h4')):
        semester = soup.find('h4').getText()
     elif "semester" in str(soup.find('h3')):
        semester = soup.find('h3').getText()
     else:  
        semester = "unidentified"
     semester = semester.replace("Sommersemester", "SoSe").replace("Wintersemester", "WiSe")
     df = df.append({"exam": text[0].getText(), "url": url,
                     "date_published": text[1].getText(),
                     "exam_review_details": text[2].getText(),
                     "semester": semester}, ignore_index=True)
    
 for col in ["exam", "url", "date_published", "exam_review_details"]:
    df[col] = df[col].str.replace("\n", " ")
 df = df[df["exam"].apply(lambda x: len(x) > 1)]
 if exam != "":
    df = df[df['exam'].str.contains(exam)]
 return df

def scrape_all_overviews(url = "https://www.wiwi.hu-berlin.de/de/studium/pa/noten", exam = ""): 
 """Scrapes all available grading overviews from the Faculty of Economics and Business Administration of the Humboldt-Universität of Berlin and return the overviews or a subset based on the entered exam specification.

 Parameters
 ----------
 url : str
     URL listing the current grading overview of the HU WiWi Faculty. Defaults to "https://www.wiwi.hu-berlin.de/de/studium/pa/noten".
 exam : str
     Exam search filter by name. Defaults to "" (no search specification).
 
 Returns
 -------
 pd.DataFrame 
      Dataframe containing an exam overview. Data columns are as follows:

        ==================  ==============================================================
        exam                The exam name (as `str`)
        date_published      Date of the grading (as `str`)
        exam_review_details Review details (as `str`)
        semester            Semester of the publication (as `str`)
        ==================  ==============================================================
 """
 urls = list_sources()
 df = pd.DataFrame(columns = ["exam", "url", "date_published", "exam_review_details", "semester"])
 for keys,values in urls.items():
   df = df.append(scrape_overview(url = values))
 if exam != "":
    df = df[df['exam'].str.contains(exam)]
    
 df = df[df["exam"].apply(lambda x: len(x) > 1)]
 df.reset_index(drop=True, inplace=True)
 return df

def _extract_pdf(url = "url"):
 '''Extracts grading details from PDFs'''
 grades = ['1.0', '1.3', '1.7', '2.0', '2.3', '2.7', '3.0', '3.3', '3.7', '4.0', '5.0']
 if "hu-berlin.de" not in url:
    results = None
 else:
    temp = pd.DataFrame()
    try: 
        temp = tabula.read_pdf(url, pages = 1, multiple_tables = False)
        temp = temp[0]
        df_index = list(temp.index.values) 
        if isinstance(df_index[0], (int, np.integer)) == False:
            temp = temp.reset_index()     
        temp.columns = ['examiner'] + temp.columns.tolist()[1:]    
        temp = temp.dropna(subset=['examiner'])
        temp = temp.dropna(axis = 1)
        temp.reset_index(drop=True, inplace=True)
        temp["examiner"][0] = temp["examiner"][0] + ";"
        temp["merged"] = temp.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
        temp["merged"] = temp["merged"].str.replace(' / ','/').str.replace('; ',';')
        results = temp["merged"][0]
        if len(temp.columns) > 14:
            results = None 
            print("Could not extract the grades from:", url)
        else: 
            results = results
    except: 
            results = None 
            print("Could not extract the grades from:", url)
    return results

def _pull_grades(df = pd.DataFrame(), url = "url"):
 '''Iterates the extraction of grading details from the PDF over the specified column, containing URLs'''
 obs = df.shape[0] 
 urls = df.url.str.count("www.").sum()
 print("The dataframe contains", obs, "rows,", urls,"contain URLs.")
 print("Next, extracting grades from the PDF files.")
 df["grades"] = df.url.apply(lambda x: _extract_pdf(url = x))
 fail = df.grades.isna().sum() - (df.shape[0] - df.url.str.count("www.").sum())
 if fail > 0:
  print(fail, "observations could not be processed.")
 return df     

def _split_grades(df = pd.DataFrame(), grades = "grades"):
 '''Splits the grades based on specified delimiter.'''
 df = df.dropna(how='all', axis=1)
 df["grades"] = df["grades"].str.strip()
 df[["examiner", "grades"]] = df.grades.str.split(';',expand=True)
 df[["round","examiner"]] = df.examiner.str.split(' ',1,expand=True) 
 cols = ['participants', '1.0', '1.3', '1.7', '2.0', '2.3', '2.7', '3.0', '3.3', '3.7', '4.0', '5.0']
 df[cols] = df[grades].str.split(' ',expand=True).replace("-", "0")
 del df["grades"]
 return df

def get_grading(exam="", only_current_semester = True):
 """Scrapes the gradings from the Faculty of Economics and Business Administration of the Humboldt-Universität of Berlin and returns an overviews or a subset based on the entered exam specification.

 Parameters
 ----------
 exam : str
     Exam search filter by name. Defaults to "" (no search specification).
 only_current_semester  : bool
     Shall only the latest available semester data be scraped? Defaults to True.
 
 Returns
 -------
 pd.DataFrame 
      Dataframe containing an exam overview. Data columns are as follows:

        ==================  =========================================================
        exam                The exam name (as `str`)
        date_published      Date of the grading (as `str`)
        exam_review_details Review details (as `str`)
        semester            Semester of the publication (as `str`)
        examiner            Name of the examiner (as `str`)
        round               Exam round '01'/'02' as prior/after the break (as `str`)
        participants        Number of participants (as `str`)
        1.0                 Number of participants with a grading of 1.0 (as `str`)
        1.3                 Number of participants with a grading of 1.3 (as `str`)
        1.7                 Number of participants with a grading of 1.7 (as `str`)
        2.0                 Number of participants with a grading of 2.0 (as `str`)
        2.3                 Number of participants with a grading of 2.3 (as `str`)
        2.7                 Number of participants with a grading of 2.7 (as `str`)
        3.0                 Number of participants with a grading of 3.0 (as `str`)
        3.3                 Number of participants with a grading of 3.3 (as `str`)
        3.7                 Number of participants with a grading of 3.7 (as `str`)
        4.0                 Number of participants with a grading of 4.0 (as `str`)
        5.0                 Number of participants with a grading of 5.0 (as `str`)
        ==================  =========================================================
 """
 if only_current_semester == True:
    df = scrape_overview(url = "https://www.wiwi.hu-berlin.de/de/studium/pa/noten", exam = exam)
 else: 
    df = scrape_all_overviews(url = "https://www.wiwi.hu-berlin.de/de/studium/pa/noten", exam = exam) 
 df = _pull_grades(df = df, url = "url")
 df = _split_grades(df = df, grades = "grades")
 return df 

def prepare_for_analysis(df = pd.DataFrame()):
 """Prepares the output of the get_grading() function for further analysis, such as visualisations, regressions or
  descriptive statistics. 

 Parameters
 ----------
 df : pd.DataFrame()
     Requires the DataFrame output of the get_grading() function. 
 
 Returns
 -------
 pd.DataFrame 
      Dataframe containing an exam overview. Data columns are as follows:

        ==================  ========================================================
        exam                The exam name (as `str`)
        semester            The corresponding semester of the publication (as `str`)
        round               Exam round '01'/'02' as prior/after the break (as `str`)
        examiner            Name of the examiner (as `str`)
        grade               Grade of a single exam participant (as `int`)
        ==================  ========================================================
 """   
 df2 = pd.DataFrame()
 for index, row in df.iterrows():
  for grade in ['1.0', '1.3', '1.7', '2.0', '2.3', '2.7', '3.0', '3.3', '3.7', '4.0', '5.0']:
    if row[grade] is not None:
      for i in range(0, int(float(row[grade]))):
           exam = row.exam.replace('- 0',' - 0').replace('-0','- 0').replace(" / ","/ ")
           exam_name = exam.split(' - 0')[0].strip()
           temp1 = pd.DataFrame({ 'exam': [exam_name],
                                  'semester': [row.semester.strip()],
                                  'round' : [row["round"]],
                                  'examiner' : [row.examiner.strip()],
                                  'grade' : float(grade)})
           df2 = df2.append(temp1)
 df2.reset_index(drop=True, inplace=True)
 return df2