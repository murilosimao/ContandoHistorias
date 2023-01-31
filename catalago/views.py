from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .forms import AvaliarReviewForm
from .models import Livro, Idioma, Genero, Autor, Review 

# Create your views here.
def index(request):
   # Realiza contagem dos principais objetos
    num_livros = Livro.objects.count()
    num_idiomas = Idioma.objects.count()
    num_generos = Genero.objects.count()

    # O metodo all é implicito por padrao
    num_autores = Autor.objects.count()

    livros = Livro.objects.all()

    # Contador de acessos por sessão
    num_acessos = request.session.get("num_acessos", 0) + 1
    request.session["num_acessos"] = num_acessos

    context = {
        'titulo': 'Contando Histórias',
        'livros': livros,
        'num_livros': num_livros,
        'num_autores': num_autores,
        'num_idiomas': num_idiomas,
        'num_generos': num_generos,
        'num_acessos': num_acessos
    }

    # Renderiza o template HTML index.html com os dados da variável context
    return render(request, 'index.html', context=context)

class AutorDetailView(generic.DetailView):
    model = Autor

class AutorListView(generic.ListView):
    model = Autor

@login_required
def sobre(request):
    return render(request, 'sobre.html')

class ReviewDetailView(LoginRequiredMixin, generic.DetailView):
  model = Review
  paginate_by = 5

class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
  model = Review
  fields = ('livro', 'resumo', 'review')
  
  def get_form(self, form_class=None):
     form = super().get_form(form_class)
     form.helper = FormHelper()
     form.helper.add_input(Submit('submit', 'Create', css_class='btn-primary'))
     return form
  
  def form_valid(self, form):
      form.instance.status = Review.ReviewStatus.EM_ANALISE
      form.instance.revisor = self.request.user
      return super().form_valid(form)

class ReviewListView(generic.ListView):
  model = Review
  queryset = Review.objects.filter(status=Review.ReviewStatus.EM_ANALISE)

class LivroListView(generic.ListView):
  model = Livro
  paginate_by = 2
  # context_object_name = 'livro_list'
  # queryset = Livro.objects.all()
  # template_name = 'livro_list.html'

def livro_detail(request, pk):
  livro = Livro.objects.get(pk)
  context = {
    'livro': livro
  }
  return render(request, 'catalago/detalhe_livro', context)

class LivroDetailView(generic.DetailView):
  model = Livro
  # context_object_name = 'livro'
  # queryset = Livro.objects.get(pk = pk)
  # template_name = 'livro_detail.html'

@permission_required('pode_avaliar_review')
def review_avaliar(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = AvaliarReviewForm(request.POST)
        if form.is_valid():
            review.status = form.cleaned_data['status']
            review.save()
            return HttpResponseRedirect(reverse('review_list'))
    else:
        form = AvaliarReviewForm()
    form.helper.form_action = reverse('review_avaliar', args=[pk])
    context = {
      'form': form,
      'review': review
    }
    return render(request, 'catalago/review_avaliar_form.html', context)

class ReviewDeleteView(PermissionRequiredMixin, generic.DeleteView):
  model = Review
  success_url = reverse_lazy('livro_list')
  permission_required = 'catalago.delete_autor'

class AutorDeleteView(PermissionRequiredMixin, generic.DeleteView):
  model = Autor
  success_url = reverse_lazy('autores')
  permission_required = 'catalago.delete_review'


  














