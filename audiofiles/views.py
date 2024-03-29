from django.shortcuts import render
from pandas import unique
from .models import AudioFiles
from .serializers import AudioFilesSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.jwt import JWTAuthentication
from rest_framework.generics import ListAPIView
# from .models import Grade, Subject, Chapter
from .serializers import GradeSerializer, SubjectSerializer, ChapterSerializer, ChaptersSerializer
from rest_framework import status
from .models import Grade, Subject, Chapter, Chapters

# Create your views here.


class selectedView(ListCreateAPIView):
    lookup_url_kwarg = "ChapterName"
    serializer_class = AudioFilesSerializer

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        queryset = AudioFiles.objects.filter(ChapterName=uid, is_approved=True)
        return queryset


class idView(APIView):

    def get(self, request, id):
        queryset = AudioFiles.objects.get(id=id)
        serializer = AudioFilesSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, id):
        if (JWTAuthentication.authenticate(self, request)):
            queryset = AudioFiles.objects.get(id=id)
            serializer = AudioFilesSerializer(queryset, data=request.data)
            if (serializer.is_valid()):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            return Response("Authentication Failed")


class AudioFilesView(ListCreateAPIView):
    serializer_class = AudioFilesSerializer

    def post(self, request):
        classname = request.data.get("grade")
        subjectname = request.data.get("subject")
        chaptername = request.data.get("chapter")
        print(request.data)
        queryset = AudioFiles.objects.get(
            Class=classname, Subject=subjectname, ChapterName=chaptername)
        print(queryset)
        serializer = AudioFilesSerializer(queryset)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = AudioFiles.objects.all()
        return queryset


class ApproveAudioFilesView(APIView):
    # authentication_classes = [JWTAuthentication]

    def post(self, request, audiofile_id):
        # if not JWTAuthentication.authenticate(self, request):
        #     return Response("Authentication Failed", status=status.HTTP_401_UNAUTHORIZED)
        print("here")
        try:
            audiofile = AudioFiles.objects.get(id=audiofile_id)
        except AudioFiles.DoesNotExist:
            return Response("Audio file not found or already approved")

        try:
            audiofiles = AudioFiles.objects.filter(
                ChapterName=audiofile.ChapterName, is_approved=True)
            for i in audiofiles:
                print (i.id)
                
            audiofiles.update(is_approved=False, is_disapproved=True)
            print("asdf")

        except AudioFiles.DoesNotExist:
            return Response("Audio file not found or already approved")

        try:
            chapter = Chapter.objects.get(
                chaptername=audiofile.ChapterName)
        except Chapter.DoesNotExist:
            return Response("Chapter has not been added by admin. Please add the chapter first", status=status.HTTP_400_BAD_REQUEST)

        chapter.is_audiofile_available = True
        chapter.is_pdf_available = True
        chapter.save()
        # Approve the audio file

        audiofile.is_approved = True
        audiofile.is_disapproved=False
        audiofile.approvedBy = request.user
        audiofile.save()

        serializer = AudioFilesSerializer(audiofile)
        return Response(serializer.data)


class DisApproveAudioFilesView(APIView):
    # authentication_classes = [JWTAuthentication]

    def post(self, request, audiofile_id):
        # if not JWTAuthentication.authenticate(self, request):
        #     return Response("Authentication Failed", status=status.HTTP_401_UNAUTHORIZED)
        print("here")
        try:
            audiofile = AudioFiles.objects.get(
                id=audiofile_id)
        except AudioFiles.DoesNotExist:
            return Response("Audio file not found or already approved")

        # Approve the audio file
        audiofile.is_approved = False

        audiofile.is_disapproved = True
        audiofile.save()

        serializer = AudioFilesSerializer(audiofile)
        return Response(serializer.data)


class ApprovedAudioFilesView(ListCreateAPIView):
    serializer_class = AudioFilesSerializer
    def get_queryset(self):
        queryset = AudioFiles.objects.filter(
            is_approved=True, is_disapproved=False)
        return queryset
    
        





class DisApprovedAudioFilesView(ListCreateAPIView):
    serializer_class = AudioFilesSerializer

    def get_queryset(self):
        queryset = AudioFiles.objects.filter(
            is_approved=False, is_disapproved=True)
        return queryset


class NotApprovedAudioFilesView(ListCreateAPIView):
    serializer_class = AudioFilesSerializer

    def get_queryset(self):
        print("asdfg")
        queryset = AudioFiles.objects.filter(
            is_approved=False, is_disapproved=False)
        return queryset


class AddAudioFilesView(ListCreateAPIView):
    serializer_class = AudioFilesSerializer

    def post(self, request, *args, **kwargs):
        audio_file = request.FILES['audio_file']
        print(audio_file)
        # Check if the audio file exists in the request
        print("sdfsdf")
        if not audio_file:
            return Response({'error': 'No audio file provided'}, status=400)

        pdf_file = request.FILES.get('PDF')
        
        if not pdf_file:
            return Response({'error': 'No PDF file provided'}, status=400)

        # # Convert 'Class
        # ' to integer
        # grade = int(request.data.get('Class', 0))
        print(audio_file)
        print(pdf_file)

        # Create a new AudioFiles object with the uploaded files and other data
        audio_file_instance = AudioFiles.objects.create(
            AudioFile=audio_file,
            PDF=pdf_file,
            Class=request.data.get('Class',''),
            Subject=request.data.get('Subject', ''),
            ChapterName=request.data.get('ChapterName', ''),
            is_approved=False,  
            Author=request.data.get('Author', ''),
            description=request.data.get('description', ''),
            References=request.data.get('References', ''),
            approvedBy=None, 
            is_disapproved=False,
        )


        # Serialize the newly created object
        serializer = AudioFilesSerializer(audio_file_instance)

        # You can handle the uploaded file here, for example, save it to a specific directory or process it in any way you need.
        # You can also create an AudioFiles object and save it to the database.
        return Response({'status': 'Ok uploaded successfully'}, status=200)


class AdminView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        # Determine the type of data being added: grade, subject, or chapter
        # 'grade', 'subject', or 'chapter'
        data_type = request.data.get('type')
        print("asdfg")
        print(request.data)
        print(data_type)

        if data_type == 'grade':
            return self.add_grade(request)
        elif data_type == 'subject':
            return self.add_subject(request)
        elif data_type == 'chapter':
            return self.add_chapter(request)
        elif data_type == 'fetchgrades':
            return self.get_grades(request)
        elif data_type == 'fetchsubjects':
            return self.get_subjects(request)
        elif data_type == 'fetchchapters':
            return self.get_chapters(request)
        elif data_type == 'fetchgradecount':
            return self.get_audiofiles_count_grade(request)
        elif data_type == 'fetchsubjectcount':
            return self.get_audiofiles_count_subject(request)
        else:
            return Response({'error': 'Invalid data type'}, status=status.HTTP_400_BAD_REQUEST)

    def add_grade(self, request):
        print("asdfgh")
        g = request.data.get('grade')
        print(g)
        grade_instance = Grade.objects.create(grade=g)
        serializer = GradeSerializer(grade_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def add_subject(self, request):
        g = request.data.get('grade')
        grade = Grade.objects.get(grade=g)

        sub_name = request.data.get('subject')
        print("in add subject:", sub_name)

        existing_subject = Subject.objects.filter(subjectname=sub_name).first()
        if existing_subject:
            existing_subject2 = grade.subjects.filter(
                subjectname=sub_name).first()
            if (existing_subject2):
                return Response({'error': 'Subject with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)


            grade.subjects.add(existing_subject)
            return Response(status=status.HTTP_200_OK)

        subject_instance = Subject.objects.create(subjectname=sub_name)
        grade.subjects.add(subject_instance)

        serializer = SubjectSerializer(subject_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def add_chapter(self, request):
        grade_id = request.data.get('grade')
        subject_id = request.data.get('subject')
        grade = Grade.objects.get(grade=grade_id)
        subject = Subject.objects.get(subjectname=subject_id)
        x = 0
        for f in grade.subjects.all():
            if f.subjectname == subject_id:
                x = x+1

        if x == 0:
            return Response({'error': "Subject doesn't exist in this grade"}, status=status.HTTP_400_BAD_REQUEST)

        chap = request.data.get('chapter')
        existing_chapter = Chapter.objects.filter(chaptername=chap).first()
        if existing_chapter:
            existing_chapter_in_subject = Chapters.objects.filter(
                grade=grade, subject=subject, chapters__chaptername=request.data.get('chapter')).first()
            if existing_chapter_in_subject:
                return Response({'error': 'Chapter with this name already exists'}, status=status.HTTP_400_BAD_REQUEST)
            existing_subject_of_grade = Chapters.objects.filter(
                grade=grade, subject=subject).first()
            if existing_subject_of_grade:
                existing_subject_of_grade.chapters.add(existing_chapter)
            chapters_instance = Chapters.objects.create(
                grade=grade, subject=subject)

            chapters_instance.chapters.add(existing_chapter)
            return Response(status=status.HTTP_200_OK)

        chapter_instance = Chapter.objects.create(
            chaptername=request.data.get('chapter'))

        existing_subject_of_grade = Chapters.objects.filter(
            grade=grade, subject=subject).first()

        serializer = ChapterSerializer(chapter_instance)
        if existing_subject_of_grade:
            existing_subject_of_grade.chapters.add(chapter_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        chapters_instance = Chapters.objects.create(
            grade=grade, subject=subject)

        chapters_instance.chapters.add(chapter_instance)
        serializer = ChaptersSerializer(chapters_instance)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_grades(self, request):
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        print(grades)
        print("fetching grades")
        return Response(serializer.data)

    def get_subjects(self, request):
        try:
            grade = Grade.objects.get(grade=request.data.get('grade'))
        except Grade.DoesNotExist:
            return Response({'error': 'Grade not found'}, status=status.HTTP_404_NOT_FOUND)

        subjects = grade.subjects.all()
        serializer = SubjectSerializer(subjects, many=True)
        print(serializer.data)
        return Response(serializer.data)

    def get_chapters(self, request):
        try:
            grade = Grade.objects.get(grade=request.data.get('grade'))
            subject = Subject.objects.get(
                subjectname=request.data.get('subject'))
        except (Grade.DoesNotExist, Subject.DoesNotExist):
            return Response({'error': 'Grade or Subject not found'}, status=status.HTTP_404_NOT_FOUND)

        chapters = Chapters.objects.get(grade=grade, subject=subject)
        if chapters:
            print(chapters.chapters)
            serializer = ChapterSerializer(chapters.chapters, many=True)
            return Response(serializer.data)
        return Response("no chapters available")

    def get_audiofiles_count_grade(self, request):

        try:
            # print("dfghjhghjk");

            grade = Grade.objects.get(grade=request.data.get('grade'))

        # Filter the Chapters model to get all chapters associated with the grade
            chapters = Chapters.objects.filter(grade=grade)
            count = 0

            for rec1 in chapters.all():
                for rec2 in rec1.chapters.all():
                    if rec2.is_audiofile_available:
                        print(rec1.subject.subjectname)
                        print(rec2.chaptername)
                        print(count)
                        count = count+1

            # audiofile_chapters = chapters.filter(chapters__is_audiofile_available=True)
            # print(audiofile_chapters)
            # print("asdfg");
            # print(audiofile_chapters)
            # print(audiofile_chapters.count())
            return Response(data=count, status=status.HTTP_200_OK)

        except Grade.DoesNotExist:
            # Handle the case where the grade with the given ID does not exist
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get_audiofiles_count_subject(self, request):

        try:
            print("asd")
            grade = Grade.objects.get(grade=request.data.get('grade'))
            subject = Subject.objects.get(
                subjectname=request.data.get('subject'))

        # Filter the Chapters model to get all chapters associated with the grade
            chapters = Chapters.objects.get(
                grade=grade, subject=subject).chapters.all()
            count = 0
            for rec in chapters:
                if rec.is_audiofile_available:
                    count = count+1
            return Response(data=count, status=status.HTTP_200_OK)

        except Grade.DoesNotExist:
            # Handle the case where the grade with the given ID does not exist
            return Response(status=status.HTTP_400_BAD_REQUEST)
