from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from models import *

def main(request):
	complaint = Complaint.objects.all()
	return render(request, "index.html", {"complaint": complaint})


# def officerDetail(request, question_id):
#     officer = get_object_or_404(Officer, pk=officer_id)
#     return render(request, 'copwatch/officer_detail.html', {'officer': officer})

class DetailView(generic.DetailView):
	model = Officer
	template_name="copwatch/officer_detail.html"
