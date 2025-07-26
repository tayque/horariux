from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models.course import Course
from .course_serializer import CourseSerializer

class CourseListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        queryset = Course.objects.all()
        year_level = self.request.query_params.get('year', None)
        if year_level is not None:
            queryset = queryset.filter(academic_year_level__year_level=year_level)
        return queryset.order_by(
            'academic_year_level__year_level',
            'academic_year_level__semester_number',
            'name'
        )
    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)

            courses_by_year = {}
            for course in serializer.data:
                year = course['academic_year_level']['year_level']
                if year not in courses_by_year:
                    courses_by_year[year] = []
                courses_by_year[year].append(course)

            return Response({
                'courses': serializer.data,
                'courses_by_year': courses_by_year,
                'available_years': sorted(courses_by_year.keys())
            })

        except Exception as e:
            import traceback
            traceback.print_exc()
            from django.http import JsonResponse
            return JsonResponse({'error': str(e)}, status=500)

