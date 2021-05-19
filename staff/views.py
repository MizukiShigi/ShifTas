from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Staff

# Create your views here.

class StaffListView(TemplateView):
    template_name = 'staff/staff_list.html'
    context = {'staffs':None, 'search':None}
    def get(self, request):
        if 'search' in request.GET:
            search_name = request.GET.get('search')
            staffs = Staff.objects.filter(name__icontains=search_name)
            self.context['search'] = search_name
        else:
            staffs = Staff.objects.all()
        self.context['staffs'] = staffs
        print(staffs)
        return render(request, self.template_name, self.context)

class StaffDetailView(TemplateView):
    template_name = 'staff/staff_detail.html'
    context = {'staff':None}
    def get(self, request, pk):
        staff = Staff.objects.get(pk=pk)
        self.context['staff'] = staff
        print(self.context)
        return render(request, self.template_name, self.context)
    