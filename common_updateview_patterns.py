# common_updateview_patterns.py
# Common patterns and use cases for UpdateView

from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Book, Author

# Pattern 1: Basic UpdateView
class BasicBookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'description']
    template_name = 'books/update.html'
    success_url = reverse_lazy('book_list')

# Pattern 2: With Permission Checking
class SecureBookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['title', 'description']
    
    def test_func(self):
        """Only allow the book's author or admin to edit."""
        book = self.get_object()
        return (
            self.request.user == book.author.user or 
            self.request.user.is_staff
        )

# Pattern 3: Dynamic Fields Based on User
class ConditionalFieldsUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'books/update.html'
    
    def get_form_class(self):
        """Return different forms based on user permissions."""
        if self.request.user.is_staff:
            # Staff can edit all fields
            fields = ['title', 'author', 'description', 'isbn', 'published_date']
        else:
            # Regular users can only edit basic info
            fields = ['title', 'description']
        
        # Dynamically create form class
        from django.forms import modelform_factory
        return modelform_factory(Book, fields=fields)

# Pattern 4: Custom Success URL Based on Data
class DynamicSuccessUrlUpdateView(UpdateView):
    model = Book
    fields = ['title', 'description']
    
    def get_success_url(self):
        """Redirect to different URLs based on conditions."""
        if self.request.user.is_staff:
            return reverse_lazy('admin_book_list')
        else:
            return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})

# Pattern 5: Multiple Models Update (Advanced)
class AuthorWithBooksUpdateView(UpdateView):
    model = Author
    fields = ['name', 'email']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Update related books if needed
        if 'update_books' in self.request.POST:
            self.object.book_set.update(
                last_author_update=timezone.now()
            )
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_books'] = self.object.book_set.all()
        return context

# Pattern 6: AJAX Support
class AjaxBookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'description']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return JSON response for AJAX requests
            from django.http import JsonResponse
            return JsonResponse({
                'success': True,
                'message': f'Book "{self.object.title}" updated successfully!',
                'book_id': self.object.pk
            })
        
        return response
    
    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
        
        return super().form_invalid(form)

# Pattern 7: With File Upload
class BookWithCoverUpdateView(UpdateView):
    model = Book
    fields = ['title', 'description', 'cover_image']
    
    def form_valid(self, form):
        # Handle file upload logic
        if 'cover_image' in self.request.FILES:
            # Delete old file if exists
            if self.object.cover_image:
                self.object.cover_image.delete()
        
        return super().form_valid(form)

# Pattern 8: Bulk Update Related Objects
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'description']
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Update all books in this category
        if form.cleaned_data['name'] != form.initial['name']:
            self.object.book_set.update(
                category_updated=True
            )
        
        return response

# What Each Method Does:
"""
Key Methods You Can Override in UpdateView:

1. get_object(self, queryset=None)
   - Retrieves the object to be updated
   - Default: Uses URL parameter 'pk' or 'slug'
   
2. get_queryset(self)
   - Returns the queryset to find the object
   - Default: Model.objects.all()
   
3. get_context_data(self, **kwargs)
   - Adds data to template context
   - Default: Adds 'object' and 'form'
   
4. get_form_class(self)
   - Returns the form class to use
   - Default: Creates form from model + fields
   
5. get_form(self, form_class=None)
   - Returns form instance
   - Default: Instantiates form_class with object data
   
6. form_valid(self, form)
   - Called when form passes validation
   - Default: Saves object and redirects
   
7. form_invalid(self, form)
   - Called when form fails validation
   - Default: Re-renders form with errors
   
8. get_success_url(self)
   - Returns URL to redirect after success
   - Default: Uses success_url or object.get_absolute_url()
"""

# Common Mistakes to Avoid:
"""
1. Forgetting CSRF token in template
2. Not specifying success_url
3. Not handling permissions (anyone can edit anything!)
4. Overriding form_valid() but forgetting to call super()
5. Using reverse() instead of reverse_lazy() in class attributes
6. Not validating that user should be able to edit this object
7. Exposing sensitive fields (like passwords) in the fields list
"""
