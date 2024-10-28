from dbm import error

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import views,hod_views,staff_views,student_views,error_views



urlpatterns = [
 path('base/',views.BASE,name='base'),
 path('',views.LOGIN,name='login'),
 path('doLogin/',views.doLogin,name='doLogin'),
 path('doLogout/',views.doLogout,name='doLogout'),
 path('profile/',views.PROFILE,name='profile'),
 path('profile/update/',views.UPDATE_PROFILE,name='profile_update'),
 path('doUpdate/',views.doUpdate,name='doUpdate'),
 path('changePassword/',views.changePassword,name='changepassword'),
 path('Dashboard/',views.Dashboard,name='dashboard'),
 path('Maintainence_Error',views.MAINTAINENCE,name='maintainence_error'), #{% url 'maintainence_error' %}


 #HOD_URLS
 path('HOD/Home',hod_views.HOME,name='hod_home'),
 path('student_add/',hod_views.student_add,name='student_add'),
 path('student_list/',hod_views.student_list,name='student_list'),
 path('Hod/Student/Edit/<str:student_id>',hod_views.STUDENT_EDIT,name='student_edit'),
 path('Hod/Student/Update',hod_views.STUDENT_UPDATE,name='student_update'),
 path('Hod/Student/Delete/<str:student_id>',hod_views.STUDENT_DELETE,name='student_delete'),
 path('Hod/Student/Student_List/Search',hod_views.STUDENT_SEARCH,name='student_search'),
 path('Hod/Home/Student/Profile/<str:student_id>',hod_views.STUDENT_PROFILE,name='student_profile'),

 path('Hod/Home/Teacher_list',hod_views.TEACHER_LIST,name='teacher_list'),
 path('Hod/Home/Teacher_add',hod_views.TEACHER_ADD,name='teacher_add'),
 path('Hod/Home/Teacher/Edit/<str:teacher_id>',hod_views.TEACHER_EDIT,name='teacher_edit'),
 path('Hod/Teacher/Update',hod_views.TEACHER_UPDATE,name='teacher_update'),
 path('Hod/Teacher/Delete/<str:teacher_id>',hod_views.TEACHER_DELETE,name='teacher_delete'),

 path('Hod/Home/Branch_list',hod_views.BRANCH_LIST,name='branch_list'),
 path('Hod/Home/Branch_add',hod_views.BRANCH_ADD,name='branch_add'),
 path('Hod/Home/Branch/Delete/<str:branch_id>',hod_views.BRANCH_DELETE,name='branch_delete'),
 path('Hod/Home/Branch/Edit/<str:branch_name>',hod_views.BRANCH_EDIT,name='branch_edit'),

 path('Hod/Home/Subject_Add',hod_views.SUBJECT_ADD,name='subject_add'),
 path('Hod/Home/Subject_List',hod_views.SUBJECT_LIST,name='subject_list'),
 path('Hod/Home/Subject_Edit/<str:subject_id>/',hod_views.SUBJECT_EDIT,name='subject_edit'),
 path('Hod/Home/Subjects/Filter',hod_views.SUBJECT_FILTER,name='subject_filter'),

 path('Hod/Home/Holidays',hod_views.HOLIDAYS,name='holidays'),
 path('Hod/Home/Holiday_Add',hod_views.HOLIDAY_ADD,name='holiday_add'),
 path('Hod/Home/Holiday_Delete/<str:holiday_id>/',hod_views.HOLIDAY_DELETE,name='holiday_delete'),

 path('Hod/Events/',hod_views.EVENTS,name='events'),
 path('Hod/Home/TimetableAdd',hod_views.TIMETABLE_ADD,name='timetableadd'),
 path('Hod/Home/Timetable/TimetableFilter',hod_views.TIMETABLE_FILTER,name='timetablefilter'),
 path('Hod/Home/Timetable/Delete<str:timetable_id>',hod_views.TIMETABLE_DELETE,name='timetabledelete'),
path('check-schedule-conflict/', hod_views.check_schedule_conflict, name='check_schedule_conflict'),
 path('Hod/Home/Timetable/AddSlot',hod_views.ADD_SLOT,name='addslot'),

 path('Hod/Home/Events/Create_event',hod_views.create_event,name='create_event'),
 path('Hod/Home/Exam_List',hod_views.EXAM_LIST,name='exam_list'),
 path('Hod/Home/Exam_List/Add_Exam_Schedule',hod_views.create_exam_schedule,name='create_exam_schedule'),
path('Hod/Home/Exam_List/delete_exam_schedule/<int:id>/', hod_views.delete_exam_schedule, name='delete_exam_schedule'),


 path('Hod/Home/Fees',hod_views.FEES,name='fees'),



 #STUDENT URLS
 path('Student/Home/',student_views.HOME,name='student_home'),
 path('Student/Home/Registeration/',student_views.REGISTRATION,name='register_student'),
 path('Student/Home/Subjects/',student_views.SUBJECTS,name='subjects'),
 path('Student/Home/Assignments/Upcomming',student_views.ASSIGNMENTS_UPCOMMING,name='assignments_upcomming'),
path('Student/Home/Assignments/Past_Due',student_views.ASSIGNMENTS_PAST_DUE,name='assignments_past_due'),
path('Student/Home/Assignments/Submitted',student_views.ASSIGNMENTS_SUBMITTED,name='assignments_submitted'),
 path('Student/Home/Assignment/Upload',student_views.ASSIGNMENT_UPLOAD,name='assignment_upload'),
 path('Student/Home/Assignment/Undo_Upload',student_views.ASSIGNMENT_UNDO_UPLOAD,name='assignment_undo_upload'),
 path('Student/Home/Holidays/',student_views.HOLIDAYS,name='holidays_student'),
path('Student/Home/Timetable/',student_views.TIMETABLE,name='timetable_student'),
 path('Student/Home/Results/',student_views.RESULTS,name='results_student'),
 path('Student/Home/Events/',student_views.EVENTS,name='=student_events'),
 path('Student/Home/Notes/Subject_Notes',student_views.SUBJECT_NOTES,name='subject_notes'),
 path('Student/Home/Notes/Practise_papers/',student_views.PRACTISE_PAPERS,name='practise_papers'),
 path('Students/Home/Accounts/Pay_Fees/',student_views.PAY_FEES,name='pay_fee'),
 path('Secured/Payments_Gateway/', views.Payments_Gateway, name='secured_payments_gateway'),
 path('Secured/Payments_Gateway/Sucess/',views.Sucess_Payments_Gateway, name='secured_payments_gateway_sucess'),
 path('Student/Home/Accounts/View_Reciepts',student_views.VIEW_RECIPES,name='view_reciepts'),
path('generate-fee-receipt/<int:fee_id>/', student_views.generate_fee_receipt, name='generate_fee_receipt'),
path('Student/Home/Results/download-results/', student_views.download_results, name='download_results'),
 path('Student/Home/Exam_List',student_views.EXAM_LIST,name='examlist_student'),






 #TEACHER URLS
 path('Teacher/Home',staff_views.HOME,name='teacher_home'),
 path('Teacher/Home/Students',staff_views.STUDENT_LIST,name='student_list_teacher'),
 path('Teacher/Home/Assingnments/Upload',staff_views.ASSIGNMENT_UPLOAD,name='assignment_upload_teacher'),
path('Teacher/Home/Assingnments/Submission',staff_views.ASSIGNMENT_SUBS,name='assignment_submission'),
 path('Teacher/Home/Assignments/Uploaded',staff_views.ASSIGNMENTS_UPLOADED,name='uploaded_assignments'),
 path('Teacher/Home/Assignment/Delete/<str:assignment_id>',staff_views.ASSIGNMENT_DELETE,name='assignment_delete_teacher'),
 path('Teacher/Home/Notes/Upload_Notes',staff_views.UPLOAD_NOTES,name='upload_notes'),
path('Teacher/Home/Notes/Uploaded_Notes',staff_views.UPLOADED_NOTES,name='uploaded_notes'),
 path('Teacher/Home/Notes/Delete/<str:note_id>',staff_views.UPLOAD_NOTES_DELETE,name='upload_notes_delete'),
 path('Teacher/Home/Results/',staff_views.RESULTS,name='results_teacher'),
path('Teacher/Home/Results/Download',staff_views.RESULTS_DOWNLOAD,name='results_download_teacher'),





 #ERROR VIEWS
 path('Error/Registration_Error/',error_views.REGISTRATION_ERROR,name='registration_error'),
 path('Error/Student_Delete_Error/',error_views.STUDENT_DELETE_ERROR,name='student_delete_error'),



 #API
path('api/chart-data/', views.chart_data, name='chart_data'),
path('events/', views.event_list, name='event_list'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),





]