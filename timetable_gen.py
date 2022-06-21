import pathlib
import csv
over_not=0
err_status=1
yes=0
time = 0
chosen_subject=''
chosen_subject_2=''
chosen_subject_3=''
lab_list=[chosen_subject,chosen_subject_2,chosen_subject_3]
error_control=1
subjects_list = []
teachers_list = []
the_teachers = []
start_hour = 9 
next_hour = 10
the_subjects=''
college_days = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
]
time_slot_list = [] 
subject_per_slot = {}
MAX_HOUR_PER_SUBJECT_LAB = 6
MAX_HOUR_PER_SUBJECT_LECTURE = 3
MAX_HOUR_PER_TEACHER = 15
subject_hour_count = {'None':0}
teachers_hour_count = {}

def fill_out_subjects_list():
    #Ask user to fill in subjects list
    subjects = input('Type all subjects you want add in subjects list and separated them by comma: ')
    
    while not subjects.strip():
        print('Subject List cannot contain blank spaces')
        subjects = input('Type all subjects you want add in subjects list and separated them by comma: ')   
    
    while ',,' in subjects:
        subjects = subjects.replace(',,',',')
    the_subjects = subjects.replace(', ', ',')
    the_subjects = the_subjects.split(',')
    for subject in the_subjects:
        subject = subject.capitalize()
        if 'lab' in subject:
            if not subject in subjects_list:
                subjects_list.append(subject)
                subject_hour_count[subject] = MAX_HOUR_PER_SUBJECT_LAB
        else:
            if not subject in subjects_list:
                subjects_list.append(subject)
                subject_hour_count[subject] = MAX_HOUR_PER_SUBJECT_LECTURE
    
          
def fill_out_teachers_list():
    #Ask user to fill in teachers list
    while True:
        if len(subjects_list)!=len(teachers_list):
            teachers_list.clear()
            teachers_hour_count.clear()
            print('Each subject should be occupied by respective teacher')
            teacher = input('Type all teachers you want add for respective subject and separate them by comma: ')
            while not teacher.strip():
                print('Teachers List cannot contain blank spaces')
                teacher = input('Type all teachers you want add for respective subject and separate them by comma: ')
            while ',,' in teacher:
                teacher = teacher.replace(',,',',')
            the_teachers = teacher.replace(', ', ',')
            the_teachers = the_teachers.split(',')
            for teacher in the_teachers:
                teacher = teacher.capitalize()
                teachers_list.append(teacher)
                teachers_hour_count[teacher] = MAX_HOUR_PER_TEACHER
        else:
            break

#Ask hour-wise subject to user\\
def ask_hour():    
    print(f'Subjects list: {subjects_list}')
    print(f'Planning time: {start_hour}h-{next_hour}h')
    user_answer = input('What\'s subject do you want put here? ')
    return user_answer

#SUBJECT OUT OF LIST CONTROL\\
def sub_list_con(chosen_subject):
    if chosen_subject!='None':
        if not chosen_subject in subjects_list :
            print(f'{chosen_subject} is not in subjects list.')
            print('Choose another subject.')
            return 1
        else:       
            return 0
    else:
        return 0

#SUBJECT TIME LIMIT CONTROL\\
def sub_time_con(chosen_subject):
    if chosen_subject!='None':
        if subject_hour_count[chosen_subject]==0:
            print('Subject\'s time is completed try entering other subjects')
            print('Remaining time for subjects : ',subject_hour_count)
            return 1
        else:       
            return 0
    else:
        return 0

#CONSECUTIVE LECTURES FOR SAME TEACHER CONTROL    &    TEACHER WORKING HOURS LIMIT CONTROL\\
def sub_rep_maxworking_con(chosen_subject,prev_hour_format,day_count):
    k=subjects_list.index(chosen_subject)
    teach=teachers_list[k]
    if chosen_subject!='None':
        if subject_per_slot.get(prev_hour_format):
            prev_sub_detail=subject_per_slot.get(prev_hour_format)
            if prev_sub_detail:
                print(prev_sub_detail)
                print(day_count)
                if prev_sub_detail[day_count]:
                    prev_sub_withteacher=prev_sub_detail[day_count]
                    if not 'lab' in prev_sub_withteacher:
                        prev_sub=prev_sub_withteacher.split(' ')
                        # print(prev_sub,"\n",prev_sub[0])
                        if teach==prev_sub[-1]:
                            print('Lectures repeated or Teacher\'s max limit reached for the day!!!')
                            return 1
                        else:       
                            return 0
                    else:       
                        return 0
                else:       
                    return 0
            else:       
                return 0            
        else:       
            return 0
    else:
        return 0

#FINAL ERROR CONTROL\\
def lab_condition(chosen_subject,max_hour_format,day_count):
    global err_status
    error_con=1
    error_con_2=1
    error_con_3=1
    if chosen_subject!='None':
        if error_con==1 or error_con_2==1 or error_con_3==1:
            error_con=sub_list_con(chosen_subject)
            if error_con==0:
                error_con_2=sub_time_con(chosen_subject)
                if error_con_2==0:
                    error_con_3=sub_rep_maxworking_con(chosen_subject,max_hour_format,day_count)
        if error_con==0 and error_con_2==0 and error_con_3==0:
            err_status=0
    else:
        err_status=0

def condition_check(prev_hour_format,max_hour_format,day_count,i):
    global lab_list
    global yes
    global err_status
    global chosen_subject
    global chosen_subject_2
    global chosen_subject_3
    global start_hour
    global next_hour
    global time
    error_control=1
    error_control_2=1
    error_control_3=1
    error_control_4=1
    while error_control==1 or error_control_2==1 or error_control_3==1 or error_control_4==1:
        if error_control==0 and error_control_2==0 and error_control_3==0 and error_control_4==0:
            break
        chosen_subject = ask_hour().capitalize()
        countt=0
        while 'lab' in chosen_subject:
            yes=0
            if time+1<i:
                if time<4:
                    if time+1<4:
                        yes=1
                elif time>4:
                    if time+1<i:
                        yes=1
                elif time==4:
                    print('No lectures/labs allowed in break!!!')
            if yes==1:
                while chosen_subject_2==chosen_subject_3 or chosen_subject_3==chosen_subject or chosen_subject==chosen_subject_2:
                    if chosen_subject_2!=chosen_subject_3 and chosen_subject_3!=chosen_subject and chosen_subject!=chosen_subject_2:
                        break
                    err_status=1
                    while err_status==1:
                        if err_status==0:
                            break
                        if countt==1:
                            chosen_subject = ask_hour().capitalize()
                        if not 'lab' in chosen_subject:
                            break
                        else:
                            print(f'start_hour: {start_hour}')
                            print(f'next_hour: {next_hour+1}')
                            lab_condition(chosen_subject,max_hour_format,day_count)
                        countt=1
                    if not 'lab' in chosen_subject:
                        break
                    print('All three batches should be given different labs')
                    print('Enter Lab subject for other 2nd Batch : ')
                    chosen_subject_2 = ask_hour().capitalize()
                    err_status=1
                    while err_status==1:
                        if err_status==0:
                            break
                        if not 'lab' in chosen_subject_2:
                            print('Enter Lab subject for other 2nd Batch : ')
                            chosen_subject_2 = ask_hour().capitalize()
                        else:
                            print(f'start_hour: {start_hour}')
                            print(f'next_hour: {next_hour+1}')
                            lab_condition(chosen_subject_2,max_hour_format,day_count)

                    print('Enter Lab subject for other 3rd Batch : ')                    
                    chosen_subject_3 = ask_hour().capitalize()
                    err_status=1
                    while err_status==1:
                        if err_status==0:
                            break
                        if not 'lab' in chosen_subject_3:
                            print('Enter Lab subject for other 3rd Batch : ') 
                            chosen_subject_3 = ask_hour().capitalize()
                        else:
                            print(f'start_hour: {start_hour}')
                            print(f'next_hour: {next_hour+1}')
                            lab_condition(chosen_subject_3,max_hour_format,day_count)
            else:
                start_hour=start_hour-1
                next_hour=next_hour-1
                time=time-1
                print(f'start_hour: {start_hour}')
                print(f'next_hour: {next_hour}')
                print('Lab subject can not be accomodated in this time')
                break    
            if chosen_subject_2!=chosen_subject_3 and chosen_subject_3!=chosen_subject and chosen_subject!=chosen_subject_2:
                lab_list=[chosen_subject,chosen_subject_2,chosen_subject_3]
                break
            if not 'lab' in chosen_subject:
                break
 
        if not 'lab' in chosen_subject:
            print(f'start_hour: {start_hour}')
            print(f'next_hour: {next_hour}')
            error_control=sub_list_con(chosen_subject)
            if error_control==0:
                error_control_2=sub_time_con(chosen_subject)
                if error_control_2==0:
                    error_control_3=sub_rep_maxworking_con(chosen_subject,prev_hour_format,day_count)
                    if error_control_3==0:
                        error_control_4=sub_rep_maxworking_con(chosen_subject,max_hour_format,day_count)
            # print(error_control,error_control_2,error_control_3,error_control_4)
        elif chosen_subject=='None':
            break
        else:
            break
        
def time_completion_check():
    global over_not
    over_not=0
    for timee in subject_hour_count.values():
        if timee<=0:
            pass
        else:
            over_not=1
            break

def insertion(hour_format):
    global start_hour
    global next_hour
    global time   
    k=subjects_list.index(lab_list[0])
    teach_1=teachers_list[k]
    k=subjects_list.index(lab_list[1])
    teach_2=teachers_list[k]
    k=subjects_list.index(lab_list[2])
    teach_3=teachers_list[k]
    for j in range(2):
        if not hour_format in time_slot_list:
            time_slot_list.append(hour_format)
            subject_per_slot[hour_format] = ['A'+' '+lab_list[0]+' '+teach_1+' '+'B'+' '+lab_list[1]+' '+teach_2+' '+'C'+' '+lab_list[2]+' '+teach_3]
        else:
            subject_per_slot[hour_format] = ['A'+' '+lab_list[0]+' '+teach_1+' '+'B'+' '+lab_list[1]+' '+teach_2+' '+'C'+' '+lab_list[2]+' '+teach_3]
                    
        for subject, max_hour in subject_hour_count.items():
            for lab in lab_list:
                if lab == subject:
                    subject_hour_count[lab] = max_hour - 1

        start_hour += 1
        next_hour += 1
        hour_format = f'{start_hour}h-{next_hour}h'
        time += 1
    

#PROGRAM STARTING FROM HERE:--
fill_out_subjects_list()
fill_out_teachers_list()
teachers_list.insert(0,'None')
subjects_list.insert(0,'None')

time_completion_check()
day_count=0
for day in college_days:
    time_completion_check()   
    i=0
    if over_not==1:
        i=int(input('College working hours on '+day+': '))
        time = 0
        start_hour = 9
        next_hour = 10
        print('\n---------------------------')
        print(f'{day.capitalize()} timetable')
        print('---------------------------\n')
        while time < i:
            time_completion_check()
            hour_format = f'{start_hour}h-{next_hour}h'
            prev_hour_format = f'{start_hour-1}h-{next_hour-1}h'
            max_hour_format =  f'{start_hour-7}h-{next_hour-7}h'
            if time == 4:
                subject_per_slot[hour_format] = ['Break time']
                if not hour_format in time_slot_list:
                    time_slot_list.append('hour_format')
            else:
                if over_not==1:
                    condition_check(prev_hour_format,max_hour_format,day_count,i)                             
                    #SUBJECT WITH TEACHER NAME ADDED TO THE TIMETABLE DICTIONARY CONTROL\\
                    if not 'lab' in chosen_subject:
                        if not hour_format in time_slot_list:
                            time_slot_list.append(hour_format)
                            k=subjects_list.index(chosen_subject)
                            teach=teachers_list[k]
                            subject_per_slot[hour_format] = [chosen_subject+' '+teach]
                        else:
                            k=subjects_list.index(chosen_subject)
                            teach=teachers_list[k]
                            subject_per_slot[hour_format] += [chosen_subject+' '+teach]       
                        for subject, max_hour in subject_hour_count.items():
                            if chosen_subject == subject:
                                subject_hour_count[chosen_subject] = max_hour - 1  
                    else:
                        if err_status==0:
                            insertion(hour_format)
                            start_hour=start_hour-1
                            next_hour=next_hour-1
                            time=time-1

            start_hour += 1
            next_hour += 1
            time += 1
    day_count+=1
    

print(f'Subject per slot: {subject_per_slot}')
timetable_path = pathlib.Path.cwd() / 'timetable.csv'
with open(timetable_path, 'w') as timetable_file:
    timetable_writing = csv.writer(timetable_file)
    csv_headers = ['Hours']
    csv_headers.extend(college_days)
    timetable_writing.writerow(csv_headers)
    for time_slot, concerned_subjects in subject_per_slot.items():
        time_line = [time_slot]
        concerned_subjects_list = []
        if concerned_subjects == ['Break time']:
            for x in range(0, len(college_days)):
                concerned_subjects_list.append('Break time')
        else:
            concerned_subjects_list = concerned_subjects
        final_line = time_line + concerned_subjects_list
        timetable_writing.writerow(final_line)
    print('Your timetable is ready')
