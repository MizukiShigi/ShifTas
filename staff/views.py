from django.shortcuts import render, redirect
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
        # print(self.context)
        return render(request, self.template_name, self.context)
    def post(self, request, pk):
        staff = Staff.objects.get(pk=pk)
        if 'edit' in request.POST:
            if 'responsible' in request.POST.getlist('check'):
                staff.responsible_flg = True
            else:
                staff.responsible_flg = False
            if 'counter' in request.POST.getlist('check'):
                staff.counter_flg = True
            else:
                staff.counter_flg = False
            if 'kitchen' in request.POST.getlist('check'):
                staff.kitchen_flg = True
            else:
                staff.kitchen_flg = False
            if 'flyer' in request.POST.getlist('check'):
                staff.flyer_flg = True
            else:
                staff.flyer_flg = False
            if 'opener' in request.POST.getlist('check'):
                staff.opener_flg = True
            else:
                staff.opener_flg = False
            if 'rookie' in request.POST.getlist('check'):
                staff.rookie_flg = True
            else:
                staff.rookie_flg = False
            staff.save()
        elif request.POST == 'delete':
            staff.delete()
        return redirect('staff_list')

            

    