from django.shortcuts import render,redirect
from django.views.generic import FormView,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction

from base.models import BaseUser
from .forms import RegisterDoctorForm
from .mixins import RegisterDoctorMixin,ConfirmDoctorMixin

# Create your views here.
class RegisterDoctorView(LoginRequiredMixin,RegisterDoctorMixin,FormView):
    form_class = RegisterDoctorForm
    template_name = "doctor/RegisterDoctor.html"
    @transaction.atomic
    def form_valid(self, form):
        user = BaseUser.objects.filter(username=self.request.user.username)
        form = form.save(commit=False)
        print(form.doc_stat)
        form.doc_stat = "requested"
        user.update(doctor_id=form.doctor_id,
                    hospital_to_request=form.hospital_to_request,
                    doc_stat="re",
                    more_info=form.more_info)
        messages.success(self.request, "request has been sent, please wait for results.")
        return redirect("base:home")
    def form_invalid(self, form):
        messages.success(self.request, "sth went wrong please try again later")
        return redirect("base:home")


class ConfirmDoctorListView(LoginRequiredMixin,ConfirmDoctorMixin, ListView):
    template_name = "doctor/ConfirmDoctor.html"
    def get_queryset(self):
        object = BaseUser.objects.filter(doc_stat="re")
        return object

class AcceptDoctorView(LoginRequiredMixin,ConfirmDoctorMixin,DetailView):
    def get(self,request,username, *args, **kwargs):
        object =BaseUser.objects.filter(username=self.kwargs['username'])
        object.update(doc_stat="ac",user_status="do")
        return redirect("doctor:confirm-doctor-page")

class DeclineDoctorView(LoginRequiredMixin,ConfirmDoctorMixin,DetailView):
    def get(self,request,username, *args, **kwargs):
        object =BaseUser.objects.filter(username=self.kwargs['username'])
        object.update(doc_stat="de",user_status="pa")
        return redirect("doctor:confirm-doctor-page")