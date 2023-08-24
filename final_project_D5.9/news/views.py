from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Post, Category
from .filters import NewsFilter
from .forms import NewForm
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class NewsListView(ListView):
    model = Post
    ordering = '-data_create'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class SearchNewsListView(ListView):
    queryset = Post.objects.filter(types='NEWS')
    ordering = '-data_create'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewDetailView(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class NewAddCreateView(CreateView, PermissionRequiredMixin):
    permission_required = ('news.add_post',)
    template_name = 'new_add.html'
    form_class = NewForm
    model = Post

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'article' in self.request.path:
            self.object.types = 'ARTI'
        return super().form_valid(form)

class NewUpdateView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    permission_required = ('news.change_post',)
    template_name = 'new_edit.html'
    form_class = NewForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewDeleteView(DeleteView):
    template_name = 'new_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'new'

def logout_user(request):
    logout(request)
    return redirect('search')

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'user_page.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context

@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/news/')

def user_page(request):
    return render(request, 'user_page.html')


class CategoryListView(NewsListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
@login_required
def subdcribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку новостей'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})
