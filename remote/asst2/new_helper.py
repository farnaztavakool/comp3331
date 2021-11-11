# COMP3311 21T3 Ass2 ... Python helper functions
# add here any functions to share between Python scripts 
# you must submit this even if you add nothing

fail = ["AF","FL","UF"]
noUOC = ["AS","AW","PW","RD","NF","LE","PE","WD","WJ"]

def getProgram(db,code):
  cur = db.cursor()
  cur.execute("select * from Programs where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStream(db,code):
  cur = db.cursor()
  cur.execute("select * from Streams where code = %s",[code])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

def getStudent(db,zid):
  cur = db.cursor()
  qry = """
  select p.*, c.name
  from   People p
         join Students s on s.id = p.id
         join Countries c on p.origin = c.id
  where  p.id = %s
  """
  cur.execute(qry,[zid])
  info = cur.fetchone()
  cur.close()
  if not info:
    return None
  else:
    return info

# query course enrolemnt for student with zid
def getEnrolment(db,zid):

  #print("Get enrolments")
  cur = db.cursor()
  enrolmentQry = "select * from course_enrolments where student = %s"
  
  # this will return student course mark grade
  cur.execute(enrolmentQry,[zid])
  info = cur.fetchall()
  #print(info)
  cur.close()

  if not info:
        return None
  else:
    #print(info)
    return info

# given the course id return course
def getCourseWithId(db,id):
  cur = db.cursor()
  courseQuery =  "select * from courses where id = %s"
  cur.execute(courseQuery,[id])
  info = cur.fetchone()
  cur.close()

  if not info:
        return None
  else:
    return info
 
#given the subject id return subject   
def getSubjectWithId(db,id):
  cur = db.cursor()
  subjectQuery = "select * from subjects where id = %s"
  cur.execute(subjectQuery,[id])
  info = cur.fetchone()
  cur.close()

  if not info:
        return None
  else:
    return info

def getSubjectWithCode(db,id):
  cur = db.cursor()
  subjectQuery = "select * from subjects where code = %s"
  cur.execute(subjectQuery,[id])
  info = cur.fetchone()
  cur.close()

  if not info:
        return None
  else:
    return info
      
# given the id return term 
def getTermWithId(db,id):
  cur = db.cursor()
  subjectQuery = "select * from terms where id = %s"
  cur.execute(subjectQuery,[id])
  info = cur.fetchone()
  cur.close()
  if not info:
        return None
  else:
    return info

def getStudentTransacript(db,zid):
  cur = db.cursor();
  query = "select code,term,name,mark,grade,uoc from Q1_helper(%s) Order By termid,code"
  cur.execute(query,[zid]);
  uoc = totalMark = 0
  for row in  cur.fetchall():
      print(f"{row[0]} {row[1]} {row[2]:<32s}",end="")
      if (row[5] not in fail and row[5] not in noUOC):
        uoc+= row[5]
      if (row[3] and row [5] not in noUOC):
        totalMark += row[3] * row[5]
      if (row[3]):
        print(f"{row[3]:>3d}  {row[4]:2s}",end="")
      else:
        print(f" -   {row[4]:2s}",end="")
      if (row[5] in fail):
        print(f" fail")
      elif (row[5] not in noUOC):
        print(f" {row[5]:2d}uoc")
  print ("UOC = ",uoc," WAM = ",totalMark/uoc)
 


def getOfferedBy(db,o_id):
    cur = db.cursor();
    query = "select name,utype from orgunits where id = %s"
    cur.execute(query,[o_id]);
    offeredBy = cur.fetchone()
    query = "select name from orgunit_types where id = %s"
    cur.execute(query,[offeredBy[1]]);
    o_type = cur.fetchone()
    if (o_type[0] in offeredBy[0]):
        return f"{offeredBy[0]}"
    return f"{o_type[0]} of {offeredBy[0]}" 

def getProgInfo(db,progInfo):
    offeredBy = getOfferedBy(db,progInfo[4])
    year = progInfo[6]/12
    print(f"{progInfo[0]} {progInfo[2]}, {progInfo[3]} UOC, {year} years \n- offered by {offeredBy}")
  
def getCourseInfo(db,courseInfo):
    offeredBy = getOfferedBy(db,courseInfo[4])
    print(f"{courseInfo[0]} {courseInfo[2]} - offered by {offeredBy}")
  

# get the rules for program
def getProgRules(code,db):
    cur = db.cursor()
    query = "select rule from program_rules where program = %s";
    cur.execute(query,[code])
    rules = []
    for info in cur.fetchall():
         query = "select * from rules where id = %s"
         #print(info)
         cur.execute(query,[info[0]])
         rules.append(cur.fetchone())
    return rules
    #print(rules)

def getRulesMain(db,rules):
    #print(rules)
    #print("prog rules",rules)
    print("Academic Requirements:")

    for rule in rules:
       # print(rule[4])
        info = getAcademicGroup(db,rule[5])
        getHeader(rule[2],rule[1],rule[3],rule[4],info[4])
        getBody(db,info[4],rule[2]);

def getAcademicGroup(db,code):
    cur = db.cursor()
    query = "select * from  academic_object_groups where id= %s";
    cur.execute(query,[code])
    return cur.fetchone()
    


# get the rules for the stream
def getStreamRules(code,db):
    cur = db.cursor()
    query = "select id from streams where code = %s"
    cur.execute(query,[code])
    stream = cur.fetchone()
    query = "select rule from stream_rules where stream = %s";
    cur.execute(query,[stream[0]])
    rules = []
    for info in cur.fetchall():
         query = "select * from rules where id = %s"
         #print(info)
         cur.execute(query,[info[0]])
         rules.append(cur.fetchone())
    return rules



 
def getHeader(rule_type,name,min_req,max_req,courses):
  if (rule_type == "DS"):
    print(f"1 stream(s) from {name}")
  if (rule_type == "CC"):
    print(f'{getCCPrefix(courses)}{name}')
  if (rule_type == "PE"):
    print(f'{getElectiveHeader(min_req,max_req)}from {name}')
  if (rule_type == "FE"):
    print( f'{getElectiveHeader(min_req,max_req)}of Free Electives')
  if (rule_type == "GE"):
    print( f'{getElectiveHeader(min_req,max_req)}of General Education')


def getElectiveHeader(min_req,max_req):

  if (not min_req and max_req):
    return f'up to {max_req} UOC '

  if (min_req and not max_req):
    return f'at least {min_req} UOC '

  if (min_req and max_req and min_req != max_req):
    return f'between {min_req} and {max_req} UOC '

  if (min_req and max_req and min_req == max_req):
    return f'{min_req} UOC '

def getCCPrefix(courses):
  if (len(courses.split(",")) > 1):
        return "all courses form "
  return ""

def getSubjectByCode(code,db):
    cur = db.cursor()
    subject_query = "select name from subjects where code = %s"
    cur.execute(subject_query,[code])
    subject_info = cur.fetchone()
    return subject_info

def getBody(db,values,rule_type):
    #print(rule_type)
    li = values.split(",")
  #print(major_list)
    cur = db.cursor()
    if (rule_type == "GE" or rule_type == "FE"):
        return 
    i = -1
    pattern_flag = False

    for code in li:
        if (rule_type == "PE" and "#" in code):
            pattern_flag = True
    #print(rule_type, pattern_flag)
    for code in li:

        i+=1
        if (pattern_flag == True):
            if ( i == 0):
                print("- courses matching ",end="")
                continue

            if (i == len(li)-1):
                print(f"{code}")
                continue

            
            print(f"{code},",end="")
            continue
            #else: 
             #   print("\n")
            
        # assumption {} only happens for subjects
        if (code.startswith("{")):
              # todo: replace this with a function
            code = code.replace("{","")
            code = code.replace("}","")
            course_list = code.split(";")
            #print(course_list[0])
            for i in range(len(course_list)):
                subject_info = getSubjectByCode(course_list[i],db)
                #print(subject_info)
                if (i == 0):
                    print( f'- {course_list[i]} {subject_info[0]}')
                else:
                    print( f'  or {course_list[i]} {subject_info[0]}')
        else:
            
            course_query = "select name from streams where code = %s"
            cur.execute(course_query,[code])
            course_info = cur.fetchone()
            subject_info = getSubjectByCode(code,db)
           #print(info)
            if (not course_info and not subject_info):
                print( f'- {code} ???')
            else:
                if (course_info):
                    print( f'- {code} {course_info[0]}')
                if (subject_info):
                     print( f'- {code} {subject_info[0]}')



'''
# name of the courses matches
def handleCC():

# course matching the pattern
def handlePE():

# courses matching FREE###, GEN###
def handleGEAndFE();
'''
def getProgression(pCode,sCode,db,zid):
      
    
    # Get the rules for the stream  
    sRules = getStreamRules(sCode,db)
    
    # Get the rules for the porgram
    pRules = getProgRules(pCode,db)
    
    # get all of the courses for rules for stream and program
    stream_courses = getCourseByRule(sRules,db)
    program_courses = getCourseByRule(pRules,db)

    res = getCourseEnrolment(zid,stream_courses,program_courses,db)
    printCompleted(res)
    printIncomplete(res,db)
    #print("this is completed \n",res["completed"])
   



def getCourseEnrolment(zid, str_courses, prog_courses,db):
    #print(str_courses)
    #print(prog_courses)
    # get the transcript
    cur = db.cursor()
    query = "select code,term,name,mark,grade,uoc from Q1_helper(%s) order By termid,code"
    cur.execute(query,[zid])
    transcript = cur.fetchall()
    
    CCs = str_courses["CC"] + prog_courses["CC"]
    print("this is str_cc",str_courses["CC"])
    print("this is prog_CC",prog_courses["CC"])
    print("this is CC",CCs)
    print(len(CCs))
    #print(CCs)
    PEs = str_courses["PE"] + prog_courses["PE"]
    PEUOC = str_courses["PEUOC"]
    PEUOC.update(prog_courses["PEUOC"])
    # free elective is from stream rules
    FEUOC = str_courses["FEUOC"]
    # general education is from prog rules
    GEUOC = prog_courses["GEUOC"]
    completed = []
    
    for row in transcript:
      #print(row)
      matchedCC = matchCC(CCs,row[0])
      if (matchedCC):
        #print("matched cc",matchedCC)
        # if matched remove the course
        if (row[4] != "FL"):
            CCs.remove(matchedCC)
        # add the course to the list of completed
        completed.append((row,matchedCC[1]))
        continue
      matchedPE = matchPE(PEs, row[0])

      if (matchedPE):
        #print(matchedPE)
        # if matched remove the course
        PEs.remove(matchedPE)
        # add the course to the list of completed
        completed.append((row,matchedPE[1]))
        # update the UOC
        #rint(PEUOC)
        updatePEUOC(PEUOC,matchedPE,row)
        continue
      
      if (row[0].startswith("GEN")):
        completed.append((row,"General Education"))

        # if matched update the UOC
        # if failed -> doesnt have an effect on UOC
        if (row[4] != "FL" ):
              GEUOC -= row[g]
       
      else:
        completed.append((row,"Free Electives"))
        # if matched update the UOC
        # if there is a min requirement and the course is not failed
        if (row[4] != "FL"):
            # if min < UOC: just set as zero
          if (FEUOC <= row[5]):
            FEUOC = 0
            continue
          # subtract the UOc
          FEUOC -= row[5]
        
              
    return {
      "completed":completed,
      "CC_incomplete": CCs,
      "PE_incomplete": PEUOC,
      "FE_incomplete": FEUOC,
      "GE_incomplete": GEUOC
    }
          
          
                
    
    
    
    
    
# handle the logic of printing out the completed courses
'''
def printQ3Completed(li):
    print("Completed:")

    # need to fix the UOC
    for i in li:
        print(f"{CourseCode} {Term} {SubjectTitle:<32s}{Mark:>3} {Grade:2s}  {UOC:2d}uoc"
'''
'''
courses: list of course codes
zid: student's zid

1) get the transcript for the student
2) if the course is in the transcript -> it is completed
3) if not: it is left to do 
4) return completed, not_completed 
'''
'''
def getCourseEnrolment(zid,course_list_rules,db):

    # get the transacript 
    completed_all = []
    not_completed_all = []
    flag = False
    cur = db.cursor()
    query = "select code,term,name,mark,grade,uoc from Q1_helper(%s) order By termid,code"
    cur.execute(query,[zid])
    transcript = cur.fetchall()
    #print("transcript: \n",cur.fetchall())
    for course_list in course_list_rules:
        completed = []
        not_completed = []
        #print("this is course_list: \n", course_list)
        for course in course_list:
            flag = False
            for row in transcript:
               if course[0] == row[0]: # if the course is in the trnsacript
                    completed.append(row+(course[1],course[2]))
                    #print(completed)
                    flag = True
                    break
            if (flag == False):
                not_completed.append(course)

        completed_all.append(completed)
        not_completed_all.append(not_completed)

    return completed_all, not_completed_all
'''
def getCourseByRule(rules,db):
    
    CC = []
    PE = []
    FE = []
    GE = []
    PEUOC = {}
    FEUOC = 0
    GEUOC = 0
    for rule in rules:
          
        info = getAcademicGroup(db,rule[5])
        
        courses = info[4].split(",")
        
        #[(course code, rule, rule name)]
        if (rule[2] == "CC"):
            CC = CC + addCourse(courses, rule)
        elif (rule[2] == "PE"):
            PE = PE + addCourse(courses,rule)
            # rule_name = min_req
            if (rule[3]):
              PEUOC [rule[1]] = rule[3]
        
        # assuming there will only be one rule for free electives
        elif (rule[2] == "FE"):
            FE = FE + addCourse(courses,rule)
            if (rule[3]):
              FEUOC = rule[3]
        # assumption: min_req == max_req == 12
        elif (rule[2] == "GE"):
            GE = GE + addCourse(courses,rule)
            GEUOC = 12

    return {
      "CC": CC,
      "PE": PE,
      "PEUOC": PEUOC,
      "FEUOC": FEUOC,
      "GEUOC": GEUOC, 
    }
   # return [CC, PE, FE, GE]
        

    
def addCourse(course_list,rule):
    li = []
    for course in course_list:
        li.append((course,rule[1],rule[0]))
    return li




def matchCC(courses,course):
  #we either have e.g: {math1231,math1131}"
  for cc in courses:
    if (cc[0].startswith("{")):
      #print(cc[0])
      trimed = cc[0].replace("{","")
      trimed = trimed.replace("}","")
      course_list = trimed.split(";")
      for i in course_list:
        if (i == course):
              return cc
    # or e.g: math 1234    
    elif(cc[0] == course):
          return cc
        
def matchPE(courses,course):
  # either match the pattern 
  for pe in courses:
    if ("#" in pe[0]):
      if (course.startswith(pe[0].split("#")[0])):
        return pe
  # match the full string
    elif(pe[0] == course):
      return pe
    
#course : transcript + rule name
def updatePEUOC(uocDict,matched,row):
    # if the course is failed ignore
    if (row[4] == "FE"): 
        return
    uoc = row[5]
    rule_name = matched[1]
    # if the rule exists in the rules 
    if (rule_name in uocDict):
      # if there is uoc left update
      if (uocDict[rule_name] > uoc):
        uocDict[rule_name] -= uoc
        return 
      # otherwise set to zero
      uocDict[rule_name] = 0
      
        
    
# if the course is failed     
def printCompleted(res):
  uocTotal = 0
  print("Completed:") # what if there is no course completed
  for row in res["completed"]:
    trans = row[0]
    rule = row[1]
    mark = "-"
    uocInformation = "fail does not count" 
    if (trans[3]):
      mark = trans[3]
    if (trans[4] != "FL"):
      uocTotal += trans[5]
      uocInformation = f"{trans[5]:2d}uoc towards {rule}"

    print(f"{trans[0]} {trans[1]} {trans[2]:<32s}{mark:>3} {trans[4]:2s}  {uocInformation}")
  print(f"UOC = {uocTotal} so far")


def printIncomplete(res,db):
  print("Remaining to complete degree:")

  # printing incomplete CCs
  for cc in res["CC_incomplete"]:
    if (cc[0].startswith("{")):
      trimed = cc[0].replace("{","")
      trimed = trimed.replace("}","")
      course_list = trimed.split(";")
      course_list_info = []
      for i in range(len(course_list)):
        info = getSubjectWithCode(db,course_list[i])
        if (i != 0):
          print(f"or {info[1]} {info[2]}")
        else:
          print(f"{info[1]} {info[2]}")

    else:
      print(f"{cc[0]} {getSubjectWithCode(db,cc[0])[2]}")
          
  # printing PE left UOCs
  # key will be the rule, value will be the UOC left
  PE = res["PE_incomplete"]
  for key in PE:
    # if min == max: x UOC of
    if (PE[key] != 0):
        print (f"at least {PE[key]} UOC courses from {key}")
    
  FE = res["FE_incomplete"]
  if (FE != 0):
    print(f"at least {FE} UOC of Free Electives")
    
  GE = res["GE_incomplete"]
  print("this is GE",GE)
  if (GE != 0):
    print(f"{GE} UOC of General Education")
