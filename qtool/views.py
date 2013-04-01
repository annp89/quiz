# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext, loader,Context
from django.forms.formsets import formset_factory, BaseFormSet
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from qtool.forms import *
from qtool.models import *

import csv




def index(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = True
	HintFormSet = formset_factory(HintForm, max_num = 10, formset = RequiredFormSet)
	VariableFormSet = formset_factory(VariableForm, max_num = 10, formset = RequiredFormSet)
	ChoiceFormSet = formset_factory(ChoiceForm, max_num = 10, formset = RequiredFormSet)
	ScriptFormSet = formset_factory(ScriptForm, max_num = 10, formset = RequiredFormSet)


	if request.method == 'POST': # If the form has been submitted...
		problem_form = ProblemForm(request.POST)
		problem_template_form = ProblemTemplateForm(request.POST, prefix='template')
		answer_form = AnswerForm(request.POST, prefix='answer')

		hint_formset = HintFormSet(request.POST, request.FILES, prefix='hints')
		variable_formset = VariableFormSet(request.POST, request.FILES, prefix='variables')
		choice_formset = ChoiceFormSet(request.POST, request.FILES, prefix='choices')
		script_formset = ScriptFormSet(request.POST, request.FILES, prefix='scripts')
		if problem_form.is_valid() and problem_template_form.is_valid() and choice_formset.is_valid() and hint_formset.is_valid() and variable_formset.is_valid() and answer_form.is_valid() and script_formset.is_valid():
			problem = problem_form.save()
			problem_template = problem_template_form.save(commit = False)
			problem_template.problem = problem
			problem_template.save()

			answer = answer_form.save(commit = False)
			answer.problem = problem
			answer.save()

            		for form in hint_formset.forms:
				hint = form.save(commit = False)
				hint.problem = problem
				hint.save()
			for form in variable_formset.forms:
				variable = form.save(commit = False)
				variable.problem = problem
				variable.save()
			for form in script_formset.forms:
				script = form.save(commit = False)
				script.problem = problem
				script.save()
			for form in choice_formset.forms:
				choice = form.save(commit = False)
				choice.problem = problem
				choice.save() # Redirect to a 'success' page
			return HttpResponseRedirect('/qtool/problems/')
	else:
	   	problem_form = ProblemForm()
		choice_formset = ChoiceFormSet(prefix='choices')
		problem_template_form = ProblemTemplateForm(prefix='template')
		answer_form = AnswerForm(prefix='answer')
		script_formset = ScriptFormSet(prefix='scripts')
		variable_formset = VariableFormSet(prefix='variables')
		hint_formset = HintFormSet(prefix='hints')
	c = {'problem_form' : problem_form,
	     'choice_formset' : choice_formset,
	     'problem_template_form' : problem_template_form,
	     'answer_form': answer_form,
	     'variable_formset' : variable_formset,
	     'script_formset' : script_formset,
	     'hint_formset' : hint_formset,
	}
	c.update(csrf(request))
	return render_to_response('qtool/add.html', c)

def edit(request, problem_id):

	problem = get_object_or_404(Problem, id=problem_id)

	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = True
	
	ProblemTemplateInlineFormSet = inlineformset_factory(Problem, ProblemTemplate, max_num =1)
	
	AnswerInlineFormSet = inlineformset_factory(Problem,Answer, max_num =1)
	VariableInlineFormSet = inlineformset_factory(Problem, Variable)

	ChoiceInlineFormSet = inlineformset_factory(Problem, Choice,)

	HintInlineFormSet = inlineformset_factory(Problem, Hint)
		
	ScriptInlineFormSet = inlineformset_factory(Problem, Script)
	if request.method == 'POST':
        	problem_form =ProblemForm(request.POST, instance=problem)
		
		problem_template_formset = ProblemTemplateInlineFormSet(request.POST, instance=problem, prefix='question')
		answer_formset = AnswerInlineFormSet(request.POST, instance=problem, prefix='answer')

	        hint_formset = HintInlineFormSet(request.POST, request.FILES, instance=problem,  prefix='hints')
	        choice_formset = ChoiceInlineFormSet(request.POST, request.FILES, instance=problem,  prefix='choices')
		script_formset = ScriptInlineFormSet(request.POST, request.FILES, instance=problem,  prefix='scripts')
	        variable_formset = VariableInlineFormSet(request.POST, request.FILES, instance=problem,  prefix='variables')
		if problem_form.is_valid() and variable_formset.is_valid() and problem_template_formset.is_valid() and choice_formset.is_valid() and hint_formset.is_valid() and answer_formset.is_valid() and script_formset.is_valid():
			problem = problem_form.save()
			problem_template_formset.save()
			answer_formset.save()
		
			variable_formset.save()
            		hint_formset.save()
			script_formset.save()
			choice_formset.save() # Redirect to a 'success' page
			return HttpResponseRedirect('/qtool/problems')
    	else:
        	problem_form = ProblemForm(instance=problem)
        	choice_formset = ChoiceInlineFormSet(instance = problem, prefix='choices')
		problem_template_formset = ProblemTemplateInlineFormSet(instance = problem, prefix='question')
		answer_formset = AnswerInlineFormSet(instance = problem, prefix='answer')
		script_formset = ScriptInlineFormSet(instance=problem, prefix='scripts')
		variable_formset = VariableInlineFormSet(instance = problem, prefix='variables')
		hint_formset = HintInlineFormSet(instance=problem, prefix='hints')
    	c = {
	'problem_form' : problem_form,
	'choice_formset' : choice_formset,
	'problem_template_formset' :problem_template_formset,
	'answer_formset': answer_formset,
	'variable_formset' : variable_formset,
	'script_formset' : script_formset,
	'hint_formset' : hint_formset,
    	}
  	c.update(csrf(request))
    	return render_to_response('qtool/edit.html', c)

def splashpage(request):
	return HttpResponseRedirect('splashpage')


def problems(request):
	problems = Problem.objects.all()
	context = Context({'problems':problems})
	return render_to_response('qtool/problems.html', context)


def problems_Summary(request):
	problems = Problem.objects.all()
	context = Context({'problems':problems})
	return render_to_response('qtool/problems_Summary.html', context)


def ka_details(request, problem_id):
	p = get_object_or_404(Problem, id=problem_id)
	q = ProblemTemplate.objects.get(problem = p)
#	v = Variable.objects.get(problem = p)
	s = Answer.objects.get(problem = p)
#	c = Choice.objects.get(problem = p)
	h = p.hint_set.all()
	context = Context({
		'p':p,
		'title':p.title,	
		'question':q,
		'solution':s,
	#	'choice':c,
#		'hint':h
	})
	return render_to_response('qtool/ka_details.html', context)

def simple_details(request, problem_id):
	p = get_object_or_404(Problem, id=problem_id)
	q = ProblemTemplate.objects.get(problem = p)
#	v = Variable.objects.get(problem = p)
	s = Answer.objects.get(problem = p)
#	c = Choice.objects.get(problem = p)
	h = p.hint_set.all()
	context = Context({
		'p':p,
		'title':p.title,	
		'question':q,
		'solution':s,
	#	'choice':c,
#		'hint':h
	})
	return render_to_response('qtool/simple_details.html', context)


def write_file(request, problem_id):
	response = HttpResponse( content_type = 'text/csv')
	s = "problem"+problem_id
	response['Content-Disposition'] = 'attachment; filename="'+s+'.csv"'

	writer = csv.writer(response)

    	problems = Problem.objects.filter(id = problem_id)        
	
    	for p in problems:
        	writer.writerow([p.title])
		writer.writerow([p.difficulty_level])
		q = ProblemTemplate.objects.get(problem = p)
		writer.writerow([q.question])
		s = Answer.objects.get(problem = p)
		writer.writerow([s.solution])

		for t in p.script_set.all():
			writer.writerow([t.script])
		for t in p.choice_set.all():
			writer.writerow([t.choice])
		for t in p.hint_set.all():
			writer.writerow([t.hint])
		for t in p.variable_set.all():
			writer.writerow([t.var_id])
			writer.writerow([t.var_value])
			writer.writerow([t.attribute])


    	return response




	
    

def delete(request, problem_id):
   p= Problem.objects.get(id = problem_id)
   p.delete()
   return HttpResponseRedirect('/qtool/problems')





def simple(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = True
	HintFormSet = formset_factory(HintForm, max_num = 10, formset = RequiredFormSet)
	ChoiceFormSet = formset_factory(ChoiceForm, max_num = 10, formset = RequiredFormSet)


	if request.method == 'POST': # If the form has been submitted...
		problem_form = SimpleProblemForm(request.POST)
		problem_template_form = ProblemTemplateForm(request.POST, prefix='template')
		answer_form = AnswerForm(request.POST, prefix='answer')

		hint_formset = HintFormSet(request.POST, request.FILES, prefix='hints')
		
		choice_formset = ChoiceFormSet(request.POST, request.FILES, prefix='choices')
		if problem_form.is_valid() and problem_template_form.is_valid() and choice_formset.is_valid() and hint_formset.is_valid() and answer_form.is_valid():
			problem = problem_form.save()
			problem_template = problem_template_form.save(commit = False)
			problem_template.problem = problem
			problem_template.save()

			answer = answer_form.save(commit = False)
			answer.problem = problem
			answer.save()

            		for form in hint_formset.forms:
				hint = form.save(commit = False)
				hint.problem = problem
				hint.save()
			for form in choice_formset.forms:
				choice = form.save(commit = False)
				choice.problem = problem
				choice.save() # Redirect to a 'success' page
			return HttpResponseRedirect('/qtool/problems')
	else:
	   	problem_form = SimpleProblemForm()
		choice_formset = ChoiceFormSet(prefix='choices')
		problem_template_form = ProblemTemplateForm(prefix='template')
		answer_form = AnswerForm(prefix='answer')
		hint_formset = HintFormSet(prefix='hints')
	c = {'problem_form' : problem_form,
	     'choice_formset' : choice_formset,
	     'problem_template_form' : problem_template_form,
	     'answer_form': answer_form,
	     'hint_formset' : hint_formset,
	}
	c.update(csrf(request))
	return render_to_response('qtool/simple.html', c)


def list(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = True
	VariableFormSet = formset_factory(VariableForm, max_num = 10, formset = RequiredFormSet)
	if request.method == 'POST': # If the form has been submitted...
		problem_form = ListProblemForm(request.POST)
		problem_template_form = ProblemTemplateForm(request.POST, prefix='template')
		answer_form = AnswerForm(request.POST, prefix='answer')
		variable_formset = VariableFormSet(request.POST,request.FILES, prefix='variables')
		if problem_form.is_valid() and problem_template_form.is_valid() and variable_formset.is_valid() and answer_form.is_valid():
			problem = problem_form.save()
			problem_template = problem_template_form.save(commit = False)
			problem_template.problem = problem
			problem_template.save()

			answer = answer_form.save(commit = False)
			answer.problem = problem
			answer.save()

            	
			for form in variable_formset.forms:
				variable = form.save(commit = False)
				variable.problem = problem
				variable.save() # Redirect to a 'success' page
			return HttpResponseRedirect('/qtool/problems')
	else:
	   	problem_form = ProblemForm()
		problem_template_form = ProblemTemplateForm(prefix='template')
		answer_form = AnswerForm(prefix='answer')	
		variable_formset = VariableFormSet(prefix='variables')
	c = {'problem_form' : problem_form,
	     'problem_template_form' : problem_template_form,
	     'answer_form': answer_form,
	     'variable_formset' : variable_formset,
	}
	c.update(csrf(request))
	return render_to_response('qtool/list.html', c)


def range(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = True
	VariableFormSet = formset_factory(VariableForm, max_num = 10, formset = RequiredFormSet)
	if request.method == 'POST': # If the form has been submitted...
		problem_form = ListProblemForm(request.POST)
		problem_template_form = ProblemTemplateForm(request.POST, prefix='template')
		answer_form = AnswerForm(request.POST, prefix='answer')
		variable_formset = VariableFormSet(request.POST,request.FILES, prefix='variables')
		if problem_form.is_valid() and problem_template_form.is_valid() and variable_formset.is_valid() and answer_form.is_valid():
			problem = problem_form.save()
			problem_template = problem_template_form.save(commit = False)
			problem_template.problem = problem
			problem_template.save()

			answer = answer_form.save(commit = False)
			answer.problem = problem
			answer.save()

            	
			for form in variable_formset.forms:
				variable = form.save(commit = False)
				variable.problem = problem
				variable.save() # Redirect to a 'success' page
			return HttpResponseRedirect('/qtool/problems')
	else:
	   	problem_form = ProblemForm()
		problem_template_form = ProblemTemplateForm(prefix='template')
		answer_form = AnswerForm(prefix='answer')	
		variable_formset = VariableFormSet(prefix='variables')
	c = {'problem_form' : problem_form,
	     'problem_template_form' : problem_template_form,
	     'answer_form': answer_form,
	     'variable_formset' : variable_formset,
	}
	c.update(csrf(request))
	return render_to_response('qtool/range.html', c)


def summative(request):
    # This class is used to make empty formset forms required
    # See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
	class RequiredFormSet(BaseFormSet):
		def __init__(self, *args, **kwargs):
			super(RequiredFormSet, self).__init__(*args, **kwargs)
			for form in self.forms:
				form.empty_permitted = True
	ProblemTemplateFormSet = formset_factory(ProblemTemplateForm, max_num = 10, formset = RequiredFormSet)
	if request.method == 'POST': # If the form has been submitted...
		problem_form = ListProblemForm(request.POST)
		problem_template_formset = ProblemTemplateFormSet(request.POST, request.FILES, prefix='template')
		if problem_form.is_valid() and problem_template_formset.is_valid():
			problem = problem_form.save()
		           	
			for form in problem_template_formset.forms:
				problem_template = form.save(commit = False)
				problem_template.problem = problem
				problem_template.save() # Redirect to a 'success' page
			return HttpResponseRedirect('/qtool/problems')
	else:
	   	problem_form = ProblemForm()
		problem_template_formset = ProblemTemplateFormSet(prefix='template')
	c = {'problem_form' : problem_form,
	     'problem_template_formset' : problem_template_formset,
	}
	c.update(csrf(request))
	return render_to_response('qtool/summative.html', c)





