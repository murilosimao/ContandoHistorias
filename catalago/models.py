from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.
class Idioma(models.Model):
    nome = models.CharField(max_length=10, help_text="Idioma de um livro")

    def __str__(self):
        return f'{self.nome}'


class Genero(models.Model):
    nome = models.CharField(max_length=10, help_text="Genero de um livro")

    def __str__(self):
        return f'{self.nome}'


class Autor(models.Model):
    primeiro_nome = models.CharField(max_length=100,
                                     help_text="Primeiro nome do autor")
    sobrenome = models.CharField(max_length=100,
                                 help_text="sobrenome do autor")
    edicao = models.CharField(max_length=10,
                              null=True,
                              help_text="edicao do livro")
    data_nascimento = models.DateField('Data de nascimento',
                                       null=True,
                                       blank=True,
                                       default=None,
                                       help_text="Data de nascimento do autor")
    data_morte = models.DateField('Data do óbito',
                                  null=True,
                                  blank=True,
                                  default=None,
                                  help_text="Data de morte do autor")

    def __str__(self):
        return f'{self.sobrenome}, {self.primeiro_nome}'


class Livro(models.Model):
    titulo = models.CharField(max_length=200, help_text="Titulo do livro")
    sumario = models.TextField(max_length=2000, help_text="Sumario do livro")
    edicao = models.CharField(max_length=20, help_text="Titulo do livro")
    isbn = models.CharField(verbose_name="ISBN",
                            max_length=13,
                            help_text="ISBN do livro",
                            unique=True)
    # Chaves estrangeiras
    idioma = models.ForeignKey(Idioma,
                               help_text="Idioma do livro",
                               on_delete=models.SET_NULL,
                               null=True)
    autor = models.ForeignKey(Autor,
                              help_text="Autor do livro",
                              on_delete=models.CASCADE,
                              null=True)
    generos = models.ManyToManyField(Genero)

    def __str__(self):
        return f'{self.titulo} - {self.autor}'

    def get_absolute_url(self):
        return reverse('livro_detail', args=[(str(self.id))])


class Review(models.Model):
    data_review = models.DateTimeField(auto_now_add=True)
    resumo = models.CharField(max_length=200, help_text="Headline da review")
    review = models.TextField(max_length=2000, help_text="Conteúdo da review")
    livro = models.ForeignKey(Livro,
                              help_text="Autor do livro",
                              on_delete=models.CASCADE)
    revisor = models.ForeignKey(User,
                                help_text="Usuário que criou a review",
                                related_name="user_revisor",
                                null=True,
                                on_delete=models.CASCADE)
    avaliador = models.ForeignKey(User,
                                  help_text="Usuário que avaliou esta review",
                                  related_name="user_avaliador",
                                  null=True,
                                  on_delete=models.SET_NULL)

    class Meta:
        permissions = (("pode_avaliar_review", "Pode avaliar uma review cadastrada"),)
    # REVIEW_STATUS = (
    #     ('e','Em análise'),
    #     ('r','Reprovada'),
    #     ('a','Aprovada'),
    # )

    class ReviewStatus(models.TextChoices):
        EM_ANALISE = 'e', "Em análise"
        REPROVADA = 'r', "Reprovada"
        APROVADA = 'a', "Aprovada"

    status = models.CharField(max_length=1,
                              help_text="Status do review",
                              default=ReviewStatus.EM_ANALISE,
                              choices=ReviewStatus.choices)

    def __str__(self):
        return f'{self.livro} - ({self.revisor}) - {self.id}'
    
    def get_absolute_url(self):
        return reverse('review_detail', args=[(str(self.id))])
